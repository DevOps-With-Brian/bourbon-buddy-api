"""init

Revision ID: 2de786054641
Revises: 
Create Date: 2024-04-21 15:29:28.379142

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '2de786054641'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adjust the bourbons table to fit the new model
    op.create_table(
        'bourbons',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('proof', sa.String, nullable=True),
    )



def downgrade() -> None:
    op.drop_table('bourbons')