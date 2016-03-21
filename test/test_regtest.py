#! /usr/bin/env python
from __future__ import absolute_import
'''Tests of joinmarket bots end-to-end (including IRC and bitcoin) '''

import subprocess
from commontest import local_command, make_wallets
import os
import pytest
import time
from joinmarket import Taker, load_program_config, IRCMessageChannel
from joinmarket import validate_address, jm_single
from joinmarket import random_nick, get_p2pk_vbyte
from joinmarket import get_log, choose_sweep_orders, choose_orders, \
    pick_order, cheapest_order_choose, weighted_order_choose, debug_dump_object
import json
import sendpayment
import bitcoin as btc

#for running bots as subprocesses
python_cmd = 'python2'
yg_cmd = 'yield-generator-basic.py'
#yg_cmd = 'yield-generator-mixdepth.py'
#yg_cmd = 'yield-generator-deluxe.py'


@pytest.mark.parametrize(
    "num_ygs, wallet_structures, mean_amt, mixdepth, sending_amt",
    [
        # basic 1sp 2yg
        (2, [[1, 0, 0, 0, 0]] * 3, 10, 0, 100000000),
        # 1sp 4yg, 2 mixdepths
        (4, [[1, 2, 0, 0, 0]] * 5, 4, 1, 1234500),
    ])
def test_sendpayment(setup_regtest, num_ygs, wallet_structures, mean_amt,
                     mixdepth, sending_amt):
    """Simplest simulation possible of sendpayment, for now.
    Just 2 yield generators run in background, only 1 utxo in
    each wallet.
    """
    log = get_log()
    #hardcoded command line options
    makercount = num_ygs
    answeryes = True
    txfee = 5000
    waittime = 5
    amount = sending_amt
    wallets = make_wallets(makercount + 1,
                           wallet_structures=wallet_structures,
                           mean_amt=mean_amt)
    #the sendpayment bot uses the last wallet in the list
    wallet = wallets[makercount]['wallet']

    yigen_procs = []
    for i in range(makercount):
        ygp = local_command([python_cmd, yg_cmd,\
                             str(wallets[i]['seed'])], bg=True)
        time.sleep(2)  #give it a chance
        yigen_procs.append(ygp)

    #A significant delay is needed to wait for the yield generators to sync
    time.sleep(20)

    destaddr = btc.privkey_to_address(os.urandom(32), get_p2pk_vbyte())
    addr_valid, errormsg = validate_address(destaddr)
    assert addr_valid, "Invalid destination address: " + destaddr + \
           ", error message: " + errormsg

    #TODO paramatetrize this as a test variable
    chooseOrdersFunc = weighted_order_choose

    jm_single().nickname = random_nick()

    log.debug('starting sendpayment')

    jm_single().bc_interface.sync_wallet(wallet)
    irc = IRCMessageChannel(jm_single().nickname)
    taker = sendpayment.SendPayment(irc, wallet, destaddr, amount, makercount,
                                    txfee, waittime, mixdepth, answeryes,
                                    chooseOrdersFunc)
    try:
        log.debug('starting irc')
        irc.run()
    except:
        log.debug('CRASHING, DUMPING EVERYTHING')
        debug_dump_object(wallet, ['addr_cache', 'keys', 'wallet_name', 'seed'])
        debug_dump_object(taker)
        import traceback
        log.debug(traceback.format_exc())
    finally:
        if any(yigen_procs):
            for ygp in yigen_procs:
                ygp.kill()
    #wait for block generation
    time.sleep(5)
    received = jm_single().bc_interface.get_received_by_addr(
        [destaddr], None)['data'][0]['balance']
    assert received == amount, "sendpayment test failed - coins not arrived, " +\
           "received: " + str(received)


@pytest.fixture(scope="module")
def setup_regtest():
    load_program_config()
