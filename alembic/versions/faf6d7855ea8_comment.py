"""comment

Revision ID: faf6d7855ea8
Revises: feffde5e042d
Create Date: 2023-12-29 10:58:22.568892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'faf6d7855ea8'
down_revision: Union[str, None] = 'feffde5e042d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "comment",
        sa.Column("id",sa.Integer, primary_key=True),
        sa.Column("text",sa.Text),
        sa.Column("post_id",sa.Integer, sa.ForeignKey('post.id'))
    )


def downgrade() -> None:
    op.drop_table('comment')
