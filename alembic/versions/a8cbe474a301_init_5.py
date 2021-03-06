"""init 5

Revision ID: a8cbe474a301
Revises: eecb1f2056a8
Create Date: 2021-09-06 15:30:13.488397

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a8cbe474a301'
down_revision = 'eecb1f2056a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('abonents', 'birthday',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('abonents', 'address',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('abonents', 'address',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('abonents', 'birthday',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###
