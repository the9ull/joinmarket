import sys
import bitcoin as btc
import pytest
import json


#TODO: fold these examples into the tx_valid.json file
@pytest.mark.parametrize(
    "tx_type, tx_id, tx_hex",
    [("simple-tx",
      "f31916a1d398a4ec18d56a311c942bb6db934cee6aa8ac30af0b30aad9efb841",
      "0100000001c74265f31fc5e24895fdc83f7157cc40045235f3a71ae326a219de9de873" +
      "0d8b010000006a473044022076055917470b7ec4f4bb008096266cf816ebb089ad983e" +
      "6a0f63340ba0e6a6cb022059ec938b996a75db10504e46830e13d399f28191b9832bd5" +
      "f61df097b9e0d47801210291941334a00959af4aa5757abf81d2a7d1aca8adb3431c67" +
      "e89419271ba71cb4feffffff023cdeeb03000000001976a914a2426748f14eba44b3f6" +
      "abba3e8bce216ea233f388acf4ebf303000000001976a914bfa366464a464005ba0df8" +
      "6024a6c3ed859f03ac88ac33280600"),
     ("3partycoinjoin",
      "d91278e125673f5b9201456b0c36efac3b2b6700fdd04fc2227352a63f941170",
      "010000000cedf1756d1d679de268a533c2d009f1d06ba8918908369c5e3b818678603a" +
      "4bcb030000006b483045022100a775815dcfaf706ee9b6e6015f162d20d227eb44cf88" +
      "93fb3ac95f910058fbd50220500f1f3de75b3bdf7f6a0949528f836c694a5bd1effedb" +
      "b02156bcb292a78e5d012102a726879b9d663467ab71726ff5469c8b0a4213a93643f6" +
      "ed739fdbb1e81ca5b9ffffffff3e0ebec9b42f30657ef187bd263c57849541014700cc" +
      "5480268dc63ce6997552070000006b4830450221008ec354dcb5d661a60651e988356a" +
      "215ccaaa688be1e78861b3b89f35e0c1bb7b02203d2117791b74ad2aa594e4dc806d03" +
      "ec2a1241c4955b013dc365b6eacc4ee6c9012102632c8b13d9b94f2226c28295b52686" +
      "4bbece7ea283a90ca001e498e2a08dbebcffffffff841e4ed900a6592687d7684ec0dd" +
      "0893d7a3b86df07bb2626a1f51ae74ee0ba6010000006a473044022017f96effaf9812" +
      "0745323859e1b52699baf0993675d028882e42310deac6921102200daaab3008e9bce1" +
      "2a3e136a7e0472a12da31121237ac382a6a64e4ab5ed2e5201210365a1491d9c10f866" +
      "0a02f47a54e5c0285f186a9f5b4cb75405548cef3427c4eeffffffff7e131188b66001" +
      "c0f5a4b45bd3503d2ce17f40e43e3803a7f30c20a8214abc95080000006a4730440220" +
      "6c21a02e4bfcce3f9a5775ce7b9033bebb354b15167dec1a1b3f0c7255633234022071" +
      "994111c455b1ddd4cd093d0d4f2ecbbf1283a0a1f982962127768e3c4e251301210394" +
      "1f5e1834e8b1c1503f2d20b3f3e06db2b80de47f7f31b4cb39f75525753822ffffffff" +
      "955544430628ea06493caa541d59374d7708dbef0e59a6653ac025f341c888c8040000" +
      "006a473044022022c2afb23a7d401cdfff735ba390fac8dd2cbde2dcce4c3a8f988dfd" +
      "a08b956c02204ba4ca6dc72993da6bf3d020530f01d7fc931ef28c78c2fa9b70657e50" +
      "8873c801210240dc515cf540c43575615f18670d3f511f6f47b719650be60183ad9f61" +
      "f805cdffffffffedf1756d1d679de268a533c2d009f1d06ba8918908369c5e3b818678" +
      "603a4bcb010000006b483045022100ee3b322aab4c77debc6ebf48967f7677c03cd5fb" +
      "df775885691f1162cca1f04f0220031a8c4017618562f4a2f4f0ece98bf13063c9e03b" +
      "720b2eb3ead0ef024bee1f012103ce920bc0f19adf76e0f8b36eb62873d3cba991ee3e" +
      "6504e0dbf114a0d5865827ffffffffa8b4085018a3e8848531eecf3164ec2b89ed5ed2" +
      "172e22a19e3343f29faa3c03050000006a47304402202ff247fb0ec1eb9fa24903957d" +
      "8973eb9a3a8e2dc4d6e6dbbb366c7563b49e680220301a0df3f1dbff1f939f14b3bf78" +
      "687d8a2da26dafcb310ade85efd9cd37bd050121038cfc01875ccaacd4863515259e52" +
      "b96188e83ca30358bce4111c4021bfc66343fffffffff5e7b4d41b53a1fce37b349d02" +
      "33aed80be2b5da0ff45c59014ed5e4ff09b0a5030000006a473044022015035665d467" +
      "19031a1e09fffb92484365a38f8c51171046bedc0eea1385cb7402200a296a8315f9a6" +
      "3fe9a7020d4fa3be20a2c0587f98ae0d8d0560985d9cfb0748012103d9537b8ccb7206" +
      "383edff317fcb1e4188036a18a84a6727104dd9b4d00638037ffffffffedf1756d1d67" +
      "9de268a533c2d009f1d06ba8918908369c5e3b818678603a4bcb000000006a47304402" +
      "200742b54bb0d8e62dbb87eaa00823152ff46106824d791bcb538e47b9f52e9df90220" +
      "705de19cdc96c9dcb9f8dfff070e780c129524a56f369dc3633f69b1472c41d2012102" +
      "90428148e18a34190de8a0b9a7ab7e9353feac7bd7bb57dde4acb2a03d1dfb94ffffff" +
      "ff841e4ed900a6592687d7684ec0dd0893d7a3b86df07bb2626a1f51ae74ee0ba60c00" +
      "00006a4730440220719b2baf0422e98d7462d120c3406e7e3657cceb8fabe84ddece55" +
      "d34affb4620220168f87c8bcd57f903104b5effc0feffe3bd776dce6c09bfda8a3a36c" +
      "95788ec701210263c387f7b141cf649a5296096976b6b622cd44a611c0e485724f9432" +
      "9cf22b79ffffffff3e0ebec9b42f30657ef187bd263c57849541014700cc5480268dc6" +
      "3ce6997552010000006a47304402206e62849a47494e9294bd7e47d87b9d32a6b69097" +
      "067184b551350b7b34291d46022017ca461f6bcceb97432e9890700a68a4df4f4c5cfd" +
      "272926af00a05dfdb3c07b0121024decad000f3aabfdac5ea8f132e457f0056b1f2cab" +
      "0c946884d2ff0afbdd68b8ffffffff7e131188b66001c0f5a4b45bd3503d2ce17f40e4" +
      "3e3803a7f30c20a8214abc95090000006b483045022100fa9c274892db835066eeac6c" +
      "8f25d9507b43c93f4557b16560745e627387d7780220461025024a97816ff0567dcdca" +
      "4702b5238894ee7028d04af48a7eb11bd3520301210391c94422cd25ee416178827513" +
      "365ee49e4b2f17cdf0b07aed04353c10e34f6dffffffff06008c8647000000001976a9" +
      "14e924c7d01f0201df5b1465aed50012c4dffa0ff988ac89ac7800000000001976a914" +
      "3dc5ae7471acbba55107b651ce20177b3b44721388ac9f258509000000001976a91400" +
      "656d12c4b48359f8637bcf96f9f02ceb2fad1c88ac4de9ec04000000001976a914f7de" +
      "454e8b402cbde90f4a325de69236040f144088ac008c8647000000001976a914b7d9f8" +
      "29f1bd6919728f91f8a10ce0ca87bde1aa88ac008c8647000000001976a914b877256a" +
      "588a315e30b2c5aec38ff70cea71dd0c88ac00000000"),
     ("4partycoinjoin",
      "55eac9d4a4159d4ba355122c6c18f85293c19ae358306a3773ec3a5d053e2f1b",
      "01000000108048bbbc26c394d45b514835d998ae2679c31cecd7623041372703f469aa" +
      "ff8e040000006b4830450220293480c5975676ddbb8b66fc6e4bc53668ae4cc59d0da5" +
      "377e520f3f360ad15e022100fe6aaf3d890570d66728210afb13e221f0405bbbf43262" +
      "16371459877531a2d80121033392a42f2a8e4e93a5d7b50b4d26eabda42e04e110e77e" +
      "22b514982a832dde92ffffffff587af588bbe3f911f8234a858cdc62a1c04c12cf09f5" +
      "95f92a7292fd3f54d17e080000006b483045022100c47a07c3dd537e1e11216dcf3440" +
      "619ec80a88d25f91f8b9de74b348947ba47902205e5a335e2c75b202b75ff8a50a2560" +
      "f49542fe4e96598be6fe77b00bc7c33484012103e21d83d80666a020c3e4657f7155ac" +
      "4572edf9fc79d59b5b69e27f23ff5f8df5ffffffff8048bbbc26c394d45b514835d998" +
      "ae2679c31cecd7623041372703f469aaff8e0b0000006b48304502202a5403bfed1826" +
      "c0d5b4143229518d6c0dc6b0881ad04e26039cef4981aa9487022100cecad7bd8fd476" +
      "2257f83080bf2f56249bb36554137e9af9c1588f8f2ed170a9012103fd52e4f1e64cdd" +
      "003528cf5f388ad455d001ea691bd02125d694117a1d481bbcffffffff8048bbbc26c3" +
      "94d45b514835d998ae2679c31cecd7623041372703f469aaff8e110000006b48304502" +
      "204e024b69b4a78ea9daa63ad1d8dba5e8729fbb61749dacc49be20053db8c02710221" +
      "00c24555b43e6e838fd7cb797cbf96c278531af29493aaf719bdfe3354941d0b320121" +
      "02a322a78564a976271153b0e289d631e5c6a217542d540c94262c40a83e48281affff" +
      "ffff8048bbbc26c394d45b514835d998ae2679c31cecd7623041372703f469aaff8e05" +
      "0000006b483045022100d3c7d326e233b2238576aecf53d5c3dfb88a3b41d815ff2cfd" +
      "c3e2c5664aa52102204f0dc1cd110e4317ab435533a4440bbdabee75f360551bb46206" +
      "79043058288801210310950ae84cfb02e24960c7227e40dedbc8804397a19e277233b1" +
      "f3ecc797fdc2ffffffff9dd9d7a38ab7f29f17c4f32ae5be1426f80ff58c158fc7c74a" +
      "afb9d53659cd05050000006b483045022100cc46ea21d4a1622cf7507ab9c96863b5fa" +
      "3744c8c4b34a74c7bfdb92af41f40702200def9598dfcae25abaac047969f231c565c0" +
      "6df6f7cb8f3c588e390049b0217801210202d1c96a5b459ca4fd430afc4d1b0e468a2a" +
      "ba84c48ab5f5ad906ec09f55cfb3ffffffff84dc724e49f71d2a82cc46d781b1f47a21" +
      "18c4056ab6dad2a83f03c7ed4a08c6040000006b483045022100ee5db129b8264b8a12" +
      "e85fbf29566ad7edb84704214ced4dbea3e628149f08af02201149ab3c4e0aa6fa48ec" +
      "4816ecefda6105a6df5838e9a6dbe235d156898d3b40012102da5240065576c7567c3e" +
      "cc8dc09f3fda64a0c6b89c3974a7506bdeb7fb440704ffffffff68e787d07a48d3ba00" +
      "d8160311ff0533684dd66c7ddba8f7d74af3862d98bd8a020000006b483045022100a8" +
      "0edec0b7a6946fbcb877f95c48e22e26710f3f7a7ec9e5dd0e7622832fca3002204a8f" +
      "ecc644f674cfa8c5ba0682318f5b6cd8cc5f0c15b70e5e423e3e0888e6550121032708" +
      "198b4c046db76f9e0ff7350d05243950738b39c431f55d85d5ec886a1389ffffffff21" +
      "57aecaef0b44114b1035d6630a436ee3a6ecbeebfca48b5ce8fa6dbc5e100700000000" +
      "6b483045022100df2085a721c026328ea6dec9307c45d5991d51f696c15896ed14d40c" +
      "dc69a3d302205a598476fa84a37c5eb70bab35d4a414fce63bc8bedec7883a724ea1f7" +
      "d4b98401210271f768f5b16806df11ee81619c1371864707de25b27df94bd4516b6680" +
      "2f0709ffffffff7cabc836092178f7325571627777476d1796e446ac8039dd706754b6" +
      "824ee723040000006a473044022036eedb5259b74f8a99cba9f4866fafce94b5b7ebf7" +
      "d248e973bdba27ac1161b202203d58951892c1680fafc77dd6ee1a9c27754018b96030" +
      "a51c8891c1f5273c077f01210271f768f5b16806df11ee81619c1371864707de25b27d" +
      "f94bd4516b66802f0709ffffffff84dc724e49f71d2a82cc46d781b1f47a2118c4056a" +
      "b6dad2a83f03c7ed4a08c6000000006a473044022014a918294f28157288ab1e66e22b" +
      "fe5e5cb92dde076e133b5d1d807bfd252048022020f8ef9d0c094b476b31f177fb083c" +
      "b6e65f5167a086fd25bebe5012e46ae8b601210271f768f5b16806df11ee81619c1371" +
      "864707de25b27df94bd4516b66802f0709ffffffff4c8670675a981c70935cbd0a0de4" +
      "98c9b28c41784d590f1b9e59930e64dd53f5020000006a473044022067b08694963116" +
      "f7d53522c2327b46150084b7b9cf5b279daa1461492dffd7010220453b1fd98cdc26fe" +
      "d9385ec578da1dd11d1ca7367ebfd5586f4ddb913feabb6c01210397db984e478086ca" +
      "f0bf90181c3c597905a52416e152bff007dffd8edf06e2deffffffff8048bbbc26c394" +
      "d45b514835d998ae2679c31cecd7623041372703f469aaff8e070000006c4930460221" +
      "0094e5123e70426ff6732bebbcaaac2d871b873880d77c71a97507a074fe1046000221" +
      "00c67b7d7663817507dd03f00fd2b690d33daa645a13b6966ec1c76e5a8df0b0a40121" +
      "035a9e5cdd37824ad390d73abf2c7bc902de6dd7e4ab92fcf4e84506747e8c6cdaffff" +
      "ffff8048bbbc26c394d45b514835d998ae2679c31cecd7623041372703f469aaff8e01" +
      "0000006b483045022100cfab7cb7b645e201515b756439ba943fecb77e68c76c482de5" +
      "225bf7a80ca94a022061600e67eaf33b59c5863de617bdb79f63e69b310710cb2b7f4f" +
      "63d9d64fb3bd012102dabd952ef6ebfe396dfd66436089f5df731dd8300ecb6d88eefe" +
      "458bc73a4c8fffffffff11565b2030be339919eaa5d1c1b47f7d265485c2e230fe44d9" +
      "5ce41f3f6d5bdc030000006b483045022021d350b215077c4b1aee83c747a0cabbe148" +
      "2fc4ccc97657f07d481df3f89d45022100b16d629e35e857506af6e8dd74373f370f4b" +
      "965f332a488878dc983f554378c40121022cde2859fb62f3b671a887fcce054626cdb2" +
      "8ed4d20d0dfcf8e0b090e2d7fe4effffffff8048bbbc26c394d45b514835d998ae2679" +
      "c31cecd7623041372703f469aaff8e0c0000006a47304402203adf6153783989ca7ec1" +
      "fa12785e5abae5c6bd8a4e26bb0c2ae0cbc4635af981022056faa34a713bede42d0efe" +
      "af84c35506f47d487bed59fba2de53167fdad64c570121025d3368bbb24f5980fc6081" +
      "d2a1e0e04675d11751a53d13d896cff7b5940ac205ffffffff1cb00400000000000019" +
      "76a9146418ea7a9cbcfbd9dfb4f552c00b834072ac833a88ac40420f00000000001976" +
      "a91492f8428eae5228083b588b330f9dfc1cccd300fc88ac40420f00000000001976a9" +
      "14871e08ec7dd94ef87fd7722ee703007badb7020d88ace8030000000000001976a914" +
      "2ced0ea9992d7e5492b9053437702c83ea0750c088ac40420f00000000001976a91449" +
      "464457f02609ba1d54153eaba614ab84d593cb88ac877fc30f000000001976a9141c20" +
      "8af75037715bdca6c42f29e104af62204e4788ac540b0000000000001976a914cfccd5" +
      "185a3c4ced7514fa584eee6ebd895c984888ac73037000000000001976a9149f0ddeb2" +
      "473d013452bce71973d7515c0b4cd5cf88ac40420f00000000001976a9142cb4e342c4" +
      "398a08397a8cedfd270e432e977da488ac09c2e005000000001976a914ca9ec96314a5" +
      "f4842e3fe33a0cf6d047a4398d0a88ac40420f00000000001976a914cd0124b0969f16" +
      "4132301032a0f99de5c8d8471e88ace9320400000000001976a9145c5f87677c7b50bc" +
      "4fe88bdec9f2221a0ca3c35088ac40420f00000000001976a914fa40beb4e557e14d5e" +
      "461c7aa66d674ea6b7ce5988ac40420f00000000001976a914564bdac0f31da4f35ce5" +
      "3c9aaef7e796ed7acdcd88ace33c2b00000000001976a9142ef77132983b843b07396b" +
      "731d213e3a60b4c6e488ac40420f00000000001976a9144aa2c6a81b4ad8c9414b1039" +
      "d5b2c51d3416233888ac40420f00000000001976a914713667aa801d3d7cbf9c3d1667" +
      "626131a9937a6288ac40420f00000000001976a9142fa24ea7272cbb3ee06beeb274b3" +
      "486c3d83f60188ac40420f00000000001976a9147c2e0ee7484234b0a20fab40855dff" +
      "93c3b195da88ac40420f00000000001976a914123d15de9b64aea49a9cf81d781fdfad" +
      "00287acf88ac40420f00000000001976a91463f456082de5dbd63c7ab9cd511813d836" +
      "a2a7cd88ac306a2e00000000001976a9144103b28ac18a4ad0ce075fe323ee3d38a95c" +
      "4d2188acc0541d00000000001976a91484d1b7dadb4638895fc5eb79145dca39daea86" +
      "ca88acb80b0000000000001976a9146baff4a7a65316aed38c032c6eded2e48111fb62" +
      "88ac34080000000000001976a914a5e54586ea1626fc90359f55fa4a291c99cffae488" +
      "accdc30100000000001976a914d547e4e5b7eb382f9309622bdf0271836083936988ac" +
      "40420f00000000001976a914a0b17374b3085de303202b29439957ccd71ba13088acde" +
      "af2600000000001976a914af4d27ced320ae73068d0e2bb2c3abfe6fbe2c6988ac0000" +
      "0000"),
     ("p2sh-in-to-p2sh-out",
      "355a6090bfdb77d1d7fd7c67ba6a711b9f493344e372928fe79ca0206b34796b",
      "0100000001b5bbd7adb1f9f6f599d8e547f7f789ba9b63da9f036e8b739477bb8295fd" +
      "4a2600000000fdfd0000473044022062a3ca46f976d4719d94fa67c9360c65b0946e3a" +
      "7877f7f2c4cc37b8c77dede302203af47e6c6ccd804726295eb99f90dc198c86414d85" +
      "7e21bc617f26903d380b0901483045022100af39dc96cf32aed7165a7644dcdfa939cb" +
      "7e6af8236126644be937ff8a10b3a10220204b03b1a6b8acc7748e3c76ee968f9e9997" +
      "a81c6e944910d2dc626133aa82bf014c695221021de4261f30b149c3f14f93b1a06a5e" +
      "96aa24780c789343f80c341043d46d700a21036daab402e66c56470eda26d981f80a1b" +
      "8f224f21fdbe64329b0481b1b37d8a0b2103c72347824e9099dbdfad5a2dac56e5d056" +
      "8c9c100caa7490f62f2731c23af27353aeffffffff028a7faf00000000001976a91472" +
      "2a53477336bd4960bed86be7fc47b8ece07ba688acbda438010000000017a9148a6425" +
      "ccc0cb64097c29579a40e733819d4e07c58700000000"),
     ("op-return-output",
      "5be05925b8ef04f326b19e2c57f9ce1f3e2024aa992dd0d744f7942e92a200a5",
      "0100000001067c0bd822cdcfabf0978bdede3a7b395a5c175219fd704b1ee47f137858" +
      "6362000000006b483045022100dffb89e46c734b6429b6322bce9b6343c98d0d9eed12" +
      "059ac2b9dfcffaa5577702204350bc86aea9a7e3b2868a643d27c5a36bd3105c8a2a2c" +
      "5daf6e8441c83c870f012102a1260627f8845765759454a2ee47603312bbd7fdad0fa0" +
      "0f3ad0cea0c5602d2cffffffff03e9690700000000001976a91497d34e7a0c8082f180" +
      "546040030afb925c0f2dd888ac0000000000000000166a146f6d6e6900000000000000" +
      "0300000000000186a0aa0a0000000000001976a91488d924f51033b74a895863a5fb57" +
      "fd545529df7d88ac00000000")])
def test_serialization_roundtrip(tx_type, tx_id, tx_hex):
    assert tx_hex == btc.serialize(btc.deserialize(tx_hex))


def test_serialization_roundtrip2():
    #Data extracted from:
    #https://github.com/bitcoin/bitcoin/blob/master/src/test/data/tx_valid.json
    #These are a variety of rather strange edge case transactions, which are
    #still valid.
    #Note that of course this is only a serialization, not validity test, so
    #only currently of very limited significance
    with open("test/tx_valid.json", "r") as f:
        json_data = f.read()
    print 'read the tx data'
    valid_txs = json.loads(json_data)
    for j in valid_txs:
        #ignore comment entries
        if len(j) < 2:
            continue
        print j
        deserialized = btc.deserialize(str(j[0]))
        print deserialized
        assert j[0] == btc.serialize(deserialized)
