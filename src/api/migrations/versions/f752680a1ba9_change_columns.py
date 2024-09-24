"""change columns

Revision ID: f752680a1ba9
Revises: 117b0038320c
Create Date: 2024-09-24 09:09:21.222239

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "f752680a1ba9"
down_revision = "117b0038320c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("llm_generation")
    op.drop_table("llm_model")
    op.drop_table("llm_endpoint")
    with op.batch_alter_table("ai_lesson", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "ask_with_history",
                sa.Integer(),
                nullable=False,
                comment="Ask with history Count",
            )
        )
        batch_op.alter_column(
            "ask_prompt",
            existing_type=mysql.INTEGER(display_width=11),
            type_=sa.Text(),
            comment="Ask Prompt",
            existing_comment="Ask count history",
            existing_nullable=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("ai_lesson", schema=None) as batch_op:
        batch_op.alter_column(
            "ask_prompt",
            existing_type=sa.Text(),
            type_=mysql.INTEGER(display_width=11),
            comment="Ask count history",
            existing_comment="Ask Prompt",
            existing_nullable=False,
        )
        batch_op.drop_column("ask_with_history")

    op.create_table(
        "llm_endpoint",
        sa.Column(
            "id", mysql.BIGINT(display_width=20), autoincrement=True, nullable=False
        ),
        sa.Column(
            "endpoint_name",
            mysql.VARCHAR(length=255),
            nullable=False,
            comment="Endpoint name",
        ),
        sa.Column(
            "endpoint_url",
            mysql.VARCHAR(length=255),
            nullable=False,
            comment="Endpoint URL",
        ),
        sa.Column(
            "endpoint_type",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
            comment="Endpoint type",
        ),
        sa.Column(
            "endpoint_key",
            mysql.VARCHAR(length=255),
            nullable=False,
            comment="Endpoint key",
        ),
        sa.Column(
            "endpoint_status",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
            comment="Endpoint status",
        ),
        sa.Column(
            "created_user_id",
            mysql.VARCHAR(length=255),
            nullable=False,
            comment="Created user ID",
        ),
        sa.Column(
            "updated_user_id",
            mysql.VARCHAR(length=255),
            nullable=False,
            comment="Updated user ID",
        ),
        sa.Column(
            "endpoint_created",
            mysql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            nullable=False,
            comment="Endpoint created",
        ),
        sa.Column(
            "endpoint_updated",
            mysql.TIMESTAMP(),
            server_default=sa.text("'0000-00-00 00:00:00'"),
            nullable=False,
            comment="Endpoint updated",
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "llm_model",
        sa.Column(
            "id", mysql.BIGINT(display_width=20), autoincrement=True, nullable=False
        ),
        sa.Column(
            "model_name",
            mysql.VARCHAR(length=255),
            nullable=False,
            comment="Model name",
        ),
        sa.Column(
            "model_type",
            mysql.VARCHAR(length=255),
            nullable=False,
            comment="Model type",
        ),
        sa.Column(
            "model_desc", mysql.TEXT(), nullable=False, comment="Model description"
        ),
        sa.Column(
            "model_status",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
            comment="Model status",
        ),
        sa.Column(
            "created_user_id",
            mysql.VARCHAR(length=255),
            nullable=False,
            comment="Created user ID",
        ),
        sa.Column(
            "updated_user_id",
            mysql.VARCHAR(length=255),
            nullable=False,
            comment="Updated user ID",
        ),
        sa.Column(
            "model_created",
            mysql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            nullable=False,
            comment="Model created",
        ),
        sa.Column(
            "model_updated",
            mysql.TIMESTAMP(),
            server_default=sa.text("'0000-00-00 00:00:00'"),
            nullable=False,
            comment="Model updated",
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "llm_generation",
        sa.Column(
            "id", mysql.BIGINT(display_width=20), autoincrement=True, nullable=False
        ),
        sa.Column(
            "model_name",
            mysql.VARCHAR(length=255),
            nullable=False,
            comment="Model name",
        ),
        sa.Column(
            "endpoint_name",
            mysql.VARCHAR(length=255),
            nullable=False,
            comment="Endpoint name",
        ),
        sa.Column(
            "generation_model",
            mysql.VARCHAR(length=255),
            nullable=False,
            comment="Generation model",
        ),
        sa.Column(
            "generation_type",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
            comment="Generation type",
        ),
        sa.Column(
            "generation_input",
            mysql.TEXT(),
            nullable=False,
            comment="Generation prompt",
        ),
        sa.Column(
            "generation_output",
            mysql.TEXT(),
            nullable=False,
            comment="Generation output",
        ),
        sa.Column(
            "generation_input_tokens",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
            comment="Generation input tokens",
        ),
        sa.Column(
            "generation_output_tokens",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
            comment="Generation output tokens",
        ),
        sa.Column(
            "generation_time_cost",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
            comment="Generation time cost",
        ),
        sa.Column(
            "course_id", mysql.VARCHAR(length=255), nullable=False, comment="Course ID"
        ),
        sa.Column(
            "lesson_id", mysql.VARCHAR(length=255), nullable=False, comment="Lesson ID"
        ),
        sa.Column(
            "script_id", mysql.VARCHAR(length=255), nullable=False, comment="Script ID"
        ),
        sa.Column(
            "user_id", mysql.VARCHAR(length=255), nullable=False, comment="User ID"
        ),
        sa.Column(
            "generation_created",
            mysql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            nullable=False,
            comment="Generation created",
        ),
        sa.Column(
            "generation_updated",
            mysql.TIMESTAMP(),
            server_default=sa.text("'0000-00-00 00:00:00'"),
            nullable=False,
            comment="Generation updated",
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    # ### end Alembic commands ###
