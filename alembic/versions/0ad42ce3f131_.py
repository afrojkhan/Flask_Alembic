"""empty message

Revision ID: 0ad42ce3f131
Revises: 
Create Date: 2023-12-29 10:36:23.938065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ad42ce3f131'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50),unique=True),
        sa.Column('email', sa.String(100)),
    )


def downgrade() -> None:
    op.drop_table('user')
