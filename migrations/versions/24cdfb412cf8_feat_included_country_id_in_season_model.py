"""feat: included country id in season model

Revision ID: 24cdfb412cf8
Revises: c3e3a396e640
Create Date: 2024-05-07 00:21:09.431943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24cdfb412cf8'
down_revision = 'c3e3a396e640'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('seasons', schema=None) as batch_op:
        batch_op.add_column(sa.Column('country_id', sa.UUID(), nullable=False))
        batch_op.create_foreign_key(None, 'countries', ['country_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('seasons', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('country_id')

    # ### end Alembic commands ###