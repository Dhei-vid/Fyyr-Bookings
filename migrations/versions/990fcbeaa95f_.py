"""empty message

Revision ID: 990fcbeaa95f
Revises: 386c749acd33
Create Date: 2022-08-12 12:15:05.777426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '990fcbeaa95f'
down_revision = '386c749acd33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('upcoming', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'upcoming')
    # ### end Alembic commands ###
