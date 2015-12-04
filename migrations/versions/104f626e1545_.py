"""empty message

Revision ID: 104f626e1545
Revises: 375111a5fd54
Create Date: 2015-12-12 13:32:13.853232

"""

# revision identifiers, used by Alembic.
revision = '104f626e1545'
down_revision = '375111a5fd54'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('job', sa.Column('container_id', sa.String(length=256), nullable=True))

def downgrade():
    op.drop_column('job', 'container_id')
