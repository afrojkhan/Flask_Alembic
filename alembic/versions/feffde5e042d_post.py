"""post

Revision ID: feffde5e042d
Revises: 0ad42ce3f131
Create Date: 2023-12-29 10:46:41.778601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'feffde5e042d'
down_revision: Union[str, None] = '0ad42ce3f131'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "post",
        sa.Column("id",sa.Integer, primary_key=True),
        sa.Column("title",sa.String(100)),
        sa.Column("content",sa.Text),
        sa.Column("user_id",sa.Integer, sa.ForeignKey('user.id')),

    )


def downgrade() -> None:
    op.drop_table("post")
