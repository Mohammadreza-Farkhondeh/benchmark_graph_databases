import arango

class ArangoDBClient():
    """A class that provides methods to connect to and manipulate an ArangoDB graph database."""

    def __init__(self, host: str, port: int, username: str, password: str, database: str):
        """Initialize the class with the connection parameters.

        Args:
            host (str): The host name or IP address of the database server.
            port (int): The port number of the database server.
            username (str): The user name for authentication.
            password (str): The password for authentication.
            database (str): The name of the database to use.
        """
        self.host = host
        self.port = port
        self.hosts = [f"http://{self.host:self.port}"]
        self.username = username
        self.password = password
        self.database = database
        self.client = arango.ArangoClient(hosts=self.hosts)
        self.db = self.client.db(name=self.database, username=self.username, password=self.password)

    
    def connect(self) -> None:
        """Connect to the database using the connection parameters.

        Raises:
            arango.exceptions.ServerConnectionError: If the connection fails.
        """
        super().connect()

    def create_edge(self, source: int, target: int, interaction: str, create_nodes: bool = False) -> None:
        """Create an edge between two nodes in the database.

        Args:
            source (int): The ID of the source node.
            target (int): The ID of the target node.
            interaction (str): The type of interaction between the nodes, such as MT, RE, or RT.
            create_nodes (bool, optional): Whether to create the source and target nodes if they do not exist. Defaults to False.

        Raises:
            arango.exceptions.DocumentInsertError: If the edge insertion fails.
            arango.exceptions.DocumentGetError: If the node retrieval fails.
            arango.exceptions.DocumentReplaceError: If the node update fails.
        """
        edges = self.db["edges"]
        edge = {"_from": f"users/{source}", "_to": f"users/{target}", "interaction": interaction}
        edges.insert(edge)
        if create_nodes:
            users = self.db["users"]
            for node_id in (source, target):
                try:
                    node = users[node_id]
                except arango.exceptions.DocumentGetError:
                    node = {"_key": str(node_id)}
                    users.insert(node)
                node["edges"] = node.get("edges", []) + [edge["_id"]]
                users.replace(node)
    
    def close(self) -> None:
        """Close the database connection."""
        super().close()
    
    def __exit__(self):
        self.close()
