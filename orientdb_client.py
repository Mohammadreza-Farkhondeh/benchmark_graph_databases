import pyorient


class OrientDBClient:
    """A class that provides methods to connect to and manipulate an OrientDB graph database."""

    def __init__(self, host: str='localhost', port: int=2424, user: str='root', password: str='root', database: str='database'):
        """Initialize the class with the connection parameters.

        Args:
            host (str): The host name or IP address of the database server.
            port (int): The port number of the database server.
            user (str): The user name for authentication.
            password (str): The password for authentication.
            database (str): The name of the database to open.
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.db = pyorient.OrientDB(host, port)
        self.connect() 

    def connect(self) -> None:
        """Connect to the database using the user and password.

        Raises:
            pyorient.PyOrientConnectionException: If the connection fails.
        """
        self.db.connect(self.user, self.password)
        self.db.db_open(self.database, self.user, self.password)
    
    def create_vertex(self, id: str) -> str:
        """Create a user vertex with given name
        Args:
            data (dict): the vertex data, such as name, username, ...
        Raises:
            pyorient.PyOrientCommandException: if the query fails.
        """
        result = self.db.record_create(-1, {"@user": {"id": id}})
        return result[0]['@rid']
    
    def create_edge(
        self, source: str, target: str, interaction: str
    ) -> str:
        """Create an edge between two nodes in the database.

        Args:
            source (int): The ID of the source node.
            target (int): The ID of the target node.
            interaction (str): The type of interaction between the nodes, such as MT, RE, or RT.
            create_nodes (bool, optional): Whether to create the source and target nodes if they do not exist. Defaults to False.

        Raises:
            pyorient.PyOrientCommandException: If the query fails.
        """
        result = self.db.command(f"CREATE EDGE {interaction} FROM (SELECT FROM user WHERE id = '{source}') TO (SELECT FROM users WHERE name = '{target}')")
        return result[0]["@rid"]

    def close(self) -> None:
        """Close the database connection."""
        self.db.close()

    def __exit__(self):
        self.close()
