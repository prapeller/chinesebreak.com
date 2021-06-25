"""empty message

Revision ID: 7abc08c97e8d
Revises: 1badee252017
Create Date: 2021-06-25 11:31:18.788713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7abc08c97e8d'
down_revision = '1badee252017'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('type', sa.Enum('mp4', 'mp3', 'png', 'jpg', 'gif', 'pdf', 'svg'), nullable=True),
    sa.Column('file_path', sa.String(length=2083), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_media_name'), 'media', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_media_name'), table_name='media')
    op.drop_table('media')
    # ### end Alembic commands ###