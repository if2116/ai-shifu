def test_get_block_list(app):
    with app.app_context():
        from flaskr.service.scenario.block_funcs import get_block_list
        from flaskr.route.common import make_common_response

        block_list = get_block_list(
            app, "c669b9eb2c6d4888a20be05904dcb477", "3dde044c4f43401fa579034400ebb11f"
        )
        app.logger.info(make_common_response(block_list))

        block_list = get_block_list(
            app, "c669b9eb2c6d4888a20be05904dcb477", "5071e9aa8d1246b5870c7970b679b7d4"
        )
        app.logger.info(make_common_response(block_list))

        block_list = get_block_list(
            app, "c669b9eb2c6d4888a20be05904dcb477", "04da30869dc04a86bea282a0abdbd195"
        )
        app.logger.info(make_common_response(block_list))
