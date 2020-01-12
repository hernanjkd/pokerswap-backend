"""empty message

Revision ID: b97d7a062fe6
Revises: f82400309456
Create Date: 2020-01-11 22:04:56.352787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b97d7a062fe6'
down_revision = 'f82400309456'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('total_swaps', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles', 'total_swaps')
    # ### end Alembic commands ###