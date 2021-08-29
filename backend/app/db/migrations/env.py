import pathlib
import sys
from alembic import context
from sqlalchemy import engine_from_config, pool

from logging.config import fileConfig
import logging

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.core.config import DATABASE_URL

# Alembic config object, which provides access to values within the .ini file
config = context.config

# interpret the config file for logging
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    """
    run migrations 'online' mode
    """
    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", str(DATABASE_URL))

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=None,
            )

            with context.begin_transaction():
                context.run_migrations()


def run_migrations_offline() -> None:
    """
    run migrations 'offline' mode
    """

    context.configure(url=str(DATABASE_URL))

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    logger.info("Running migrations offline")

    run_migrations_offline()

else:
    logger.info("Running migrations online")

    run_migrations_online()
