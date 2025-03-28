from flask import Flask, request
from flaskr.service.common.models import raise_param_error
from .common import bypass_token_validation, make_common_response
from ..service.rag.funs import (
    get_kb_list,
    kb_add,
    kb_update,
    kb_look,
    kb_drop,
    oss_file_upload,
    kb_file_upload,
    retrieval,
)


def register_rag_handler(app: Flask, path_prefix: str) -> Flask:
    @app.route(path_prefix + "/kb-list", methods=["POST"])
    @bypass_token_validation
    def run_kb_list():
        """
        获取知识库列表
        ---
        tags:
            - 知识库
        parameters:
            - name: course_id_list
              in: query
              description: 根据课程ID列表进行筛选
              required: false
              schema:
                type: list
        responses:
            200:
                description: 操作成功
                content:
                    application/json:
                        schema:
                            properties:
                                code:
                                    type: integer
                                    description: 返回码
                                message:
                                    type: string
                                    description: 返回信息
                                data:
                                    type: list
                                    description: 知识库ID列表
        """
        tag_id_list = request.get_json().get("tag_id_list", [])
        course_id_list = request.get_json().get("course_id_list", [])
        app.logger.info(f"tag_id_list: {tag_id_list}")
        app.logger.info(f"course_id_list: {course_id_list}")
        if tag_id_list:
            tag_id_list = [x for x in tag_id_list if len(x) >= 32]
        if course_id_list:
            course_id_list = [x for x in course_id_list if len(x) >= 32]
        app.logger.info(f"filter tag_id_list: {tag_id_list}")
        app.logger.info(f"filter course_id_list: {course_id_list}")
        return make_common_response(
            get_kb_list(
                app,
                tag_id_list,
                course_id_list,
            )
        )

    @app.route(path_prefix + "/kb-add", methods=["POST"])
    def run_kb_add():
        """
        创建知识库
        ---
        tags:
        - 知识库
        parameters:
            - name: kb_name
              in: query
              description: 知识库名称
              required: true
              schema:
                type: string
            - name: kb_description
              in: query
              description: 知识库描述
              required: false
              schema:
                type: string
            - name: embedding_model
              in: query
              description: Embedding模型名称
              required: false
              schema:
                type: string
            - name: dim
              in: query
              description: 向量维度
              required: false
              schema:
                type: int
            - name: course_id_list
              in: query
              description: 关联课程ID列表
              required: false
              schema:
                type: list
        responses:
            200:
                description: 操作成功
                content:
                    application/json:
                        schema:
                            properties:
                                code:
                                    type: integer
                                    description: 返回码
                                message:
                                    type: string
                                    description: 返回信息
                                data:
                                    type: boolean
                                    description: 返回结果
        """
        kb_name = request.get_json().get("kb_name")
        if not kb_name:
            raise_param_error("kb_name is not found")
        kb_description = request.get_json().get("kb_description", "")
        embedding_model = request.get_json().get("embedding_model", None)
        dim = request.get_json().get("dim", None)
        if embedding_model is None and dim is None:
            embedding_model = app.config["DEFAULT_EMBEDDING_MODEL"]
            dim = app.config["DEFAULT_EMBEDDING_MODEL_DIM"]
        elif embedding_model is None or dim is None:
            raise_param_error("embedding_model or dim is not found")
        if isinstance(dim, str):
            dim = int(dim)
        if not isinstance(dim, int):
            raise_param_error("dim data type is not found")
        tag_id_list = request.get_json().get("tag_id_list", [])
        course_id_list = request.get_json().get("course_id_list", [])
        user_id = request.user.user_id
        app.logger.info(f"kb_name: {kb_name}")
        app.logger.info(f"embedding_model: {embedding_model}")
        app.logger.info(f"dim: {dim}")
        app.logger.info(f"tag_id_list: {tag_id_list}")
        app.logger.info(f"course_id_list: {course_id_list}")
        app.logger.info(f"user_id: {user_id}")
        return make_common_response(
            kb_add(
                app,
                kb_name,
                kb_description,
                embedding_model,
                dim,
                tag_id_list,
                course_id_list,
                user_id,
            )
        )

    @app.route(path_prefix + "/kb-update", methods=["POST"])
    def run_kb_update():
        """
        更新知识库
        ---
        tags:
        - 知识库
        parameters:
            - name: kb_id
              in: query
              description: 知识库ID
              required: true
              schema:
                type: string
            - name: kb_name
              in: query
              description: 知识库名称
              required: false
              schema:
                type: string
            - name: kb_description
              in: query
              description: 知识库描述
              required: false
              schema:
                type: string
            - name: embedding_model
              in: query
              description: Embedding模型名称
              required: false
              schema:
                type: string
            - name: course_id_list
              in: query
              description: 关联课程ID列表
              required: false
              schema:
                type: list
        responses:
            200:
                description: 操作成功
                content:
                    application/json:
                        schema:
                            properties:
                                code:
                                    type: integer
                                    description: 返回码
                                message:
                                    type: string
                                    description: 返回信息
                                data:
                                    type: boolean
                                    description: 返回结果
        """
        kb_id = request.get_json().get("kb_id")
        if not kb_id:
            raise_param_error("kb_id is not found")
        dim = request.get_json().get("dim", None)
        if dim is not None:
            raise_param_error("dim does not support being modified")
        kb_name = request.get_json().get("kb_name", None)
        kb_description = request.get_json().get("kb_description", None)
        embedding_model = request.get_json().get("embedding_model", None)
        tag_id_list = request.get_json().get("tag_id_list", None)
        course_id_list = request.get_json().get("course_id_list", None)
        user_id = request.user.user_id
        app.logger.info(f"kb_name: {kb_name}")
        app.logger.info(f"kb_description: {kb_description}")
        app.logger.info(f"embedding_model: {embedding_model}")
        app.logger.info(f"tag_id_list: {tag_id_list}")
        app.logger.info(f"course_id_list: {course_id_list}")
        app.logger.info(f"user_id: {user_id}")
        return make_common_response(
            kb_update(
                app,
                kb_id,
                kb_name,
                kb_description,
                embedding_model,
                tag_id_list,
                course_id_list,
                user_id,
            )
        )

    @app.route(path_prefix + "/kb-look", methods=["GET"])
    @bypass_token_validation
    def run_kb_look():
        """
        查看知识库信息
        ---
        tags:
        - 知识库
        parameters:
            - name: kb_id
              in: query
              description: 知识库ID
              required: true
              schema:
                type: str
        responses:
            200:
                description: 操作成功
                content:
                    application/json:
                        schema:
                            properties:
                                code:
                                    type: integer
                                    description: 返回码
                                message:
                                    type: string
                                    description: 返回信息
                                data:
                                    type: dict
                                    description: 返回知识库相关信息
        """
        kb_id = request.args.get("kb_id")
        if not kb_id:
            raise_param_error("kb_id is not found")
        app.logger.info(f"kb_id: {kb_id}")
        return make_common_response(
            kb_look(
                app,
                kb_id,
            )
        )

    @app.route(path_prefix + "/kb-drop", methods=["POST"])
    @bypass_token_validation
    def run_kb_drop():
        """
        删除知识库
        ---
        tags:
        - 知识库
        parameters:
            - name: kb_id_list
              in: query
              description: 知识库ID列表
              required: true
              schema:
                type: list
        responses:
            200:
                description: 操作成功
                content:
                    application/json:
                        schema:
                            properties:
                                code:
                                    type: integer
                                    description: 返回码
                                message:
                                    type: string
                                    description: 返回信息
                                data:
                                    type: boolean
                                    description: 返回结果
        """
        kb_id_list = request.get_json().get("kb_id_list")
        if not kb_id_list:
            raise_param_error("kb_id_list is not found")
        app.logger.info(f"kb_id_list: {kb_id_list}")
        return make_common_response(
            kb_drop(
                app,
                kb_id_list,
            )
        )

    @app.route(path_prefix + "/oss-file-upload", methods=["POST"])
    @bypass_token_validation
    def run_oss_file_upload():
        """
        OSS文件上传
        ---
        tags:
            - 知识库
        parameters:
            - in: formData
              name: upload_file
              type: file
              required: true
              description: 文件
        responses:
            200:
                description: 操作成功
                content:
                    application/json:
                        schema:
                            properties:
                                code:
                                    type: integer
                                    description: 返回码
                                message:
                                    type: string
                                    description: 返回信息
                                data:
                                    type: string
                                    description: OSS文件KEY
        """
        app.logger.info("enter file_upload!")
        upload_file = request.files.get("upload_file", None)
        if not upload_file:
            raise_param_error("upload_file")
        return make_common_response(oss_file_upload(app, upload_file))

    @app.route(path_prefix + "/kb-file-upload", methods=["POST"])
    @bypass_token_validation
    def run_kb_file_upload():
        """
        知识库文件上传
        ---
        tags:
        - 知识库
        parameters:
            - name: kb_id
              in: query
              description: 知识库ID
              required: true
              schema:
                type: string
            - name: file_key
              in: query
              description: OSS文件KEY
              required: true
              schema:
                type: string
            - name: split_separator
              in: query
              description: 分段标识符
              required: false
              schema:
                type: string
            - name: lesson_id
              in: query
              description: 关联章节ID
              required: false
              schema:
                type: string
        responses:
            200:
                description: 操作成功
                content:
                    application/json:
                        schema:
                            properties:
                                code:
                                    type: integer
                                    description: 返回码
                                message:
                                    type: string
                                    description: 返回信息
                                data:
                                    type: list
                                    description: 测试返回结果
        """
        kb_id = request.get_json().get("kb_id", None)
        if not kb_id:
            raise_param_error("kb_id is not found")
        file_key = request.get_json().get("file_key", None)
        if not file_key:
            raise_param_error("file_key is not found")
        split_separator = request.get_json().get("split_separator", "\n\n")
        split_max_length = request.get_json().get("split_max_length", 500)
        split_chunk_overlap = request.get_json().get("split_chunk_overlap", 50)
        lesson_id = request.get_json().get("lesson_id", "")
        app.logger.info(f"file_key: {file_key}")
        app.logger.info(f"split_separator: {split_separator}")
        app.logger.info(f"split_max_length: {split_max_length}")
        app.logger.info(f"split_chunk_overlap: {split_chunk_overlap}")
        app.logger.info(f"lesson_id: {lesson_id}")
        return make_common_response(
            kb_file_upload(
                app,
                kb_id,
                file_key,
                split_separator,
                split_max_length,
                split_chunk_overlap,
                lesson_id,
            )
        )

    @app.route(path_prefix + "/retrieval", methods=["POST"])
    @bypass_token_validation
    def run_retrieval():
        """
        知识检索
        ---
        tags:
        - 知识库
        parameters:
            - name: kb_id
              in: query
              description: 知识库ID
              required: true
              schema:
                type: string
            - name: query
              in: query
              description: 查询文本
              required: true
              schema:
                type: string
            - name: filter
              in: query
              description: 查询条件
              required: false
              schema:
                type: list
            - name: limit
              in: query
              description: 条数限制
              required: false
              schema:
                type: int
            - name: output_fields
              in: query
              description: 输出字段列表
              required: false
              schema:
                type: list
        responses:
            200:
                description: 操作成功
                content:
                    application/json:
                        schema:
                            properties:
                                code:
                                    type: integer
                                    description: 返回码
                                message:
                                    type: string
                                    description: 返回信息
                                data:
                                    type: string
                                    description: 检索结果
        """
        kb_id = request.get_json().get("kb_id")
        if not kb_id:
            raise_param_error("kb_id is not found")
        query = request.get_json().get("query")
        if not query:
            raise_param_error("query is not found")
        my_filter = request.get_json().get("filter")
        limit = request.get_json().get("limit", 3)
        output_fields = request.get_json().get("output_fields", ["text"])
        app.logger.info(f"kb_id: {kb_id}")
        app.logger.info(f"query: {query}")
        return make_common_response(
            retrieval(
                app,
                kb_id,
                query,
                my_filter,
                limit,
                output_fields,
            )
        )

    return app
