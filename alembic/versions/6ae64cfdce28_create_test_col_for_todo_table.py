"""create test col for todo table

Revision ID: 6ae64cfdce28
Revises: 
Create Date: 2023-01-12 17:14:08.132836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ae64cfdce28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('todos', sa.Column('test_col', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('todos', 'test_col')
