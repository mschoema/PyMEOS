import asyncpg

from pymeos import TBool, TInt, TFloat, TText, TGeomPoint, TGeogPoint, TBox, STBox, TimestampSet, Period, PeriodSet


class MobilityDB:
    """
    Helper class to register MobilityDB classes to an asyncpg connection and their automatic conversion to
    PyMEOS classes.
    """
    @classmethod
    async def connect(cls, *args, **kwargs) -> asyncpg.connection.Connection:
        """
        A coroutine to establish a connection to a MobilityDB server.

        Refer to :func:`asyncpg.connection.connect` for the list of valid arguments.

        If the connection already exists, see the :func:`~pymeos.db.asyncpg.MobilityDB.register` in this class.

        Args:
            *args: positional arguments that will be passed to :func:`asyncpg.connection.connect`
            **kwargs: keyword arguments that will be passed to :func:`asyncpg.connection.connect`

        Returns:
            A new :class:`asyncpg.connection.Connection` object with the MobilityDB classes registered.

        """
        conn = await asyncpg.connect(*args, **kwargs)
        await cls.register(conn)
        return conn

    @classmethod
    async def register(cls, connection: asyncpg.connection.Connection) -> None:
        """
        Registers MobilityDB classes to the passed connection.

        Args:
            connection: An :class:`asyncpg.connection.Connection` to register the classes to.
        """
        classes = [TimestampSet, Period, PeriodSet, TBox, TBool, TInt, TFloat, TText, STBox, TGeomPoint, TGeogPoint]
        for cl in classes:
            await connection.set_type_codec(cl.__name__.lower(), encoder=str, decoder=cl.read_from_cursor)
