import pyTigerGraph as tg

class TigerGraphClient():
    """A class that provides methods to connect to and manipulate a TigerGraph graph database."""

    def __init__(self, host: str, graphname: str, username: str, password: str, secret: str):
        """Initialize the class with the connection parameters.

        Args:
            host (str): The host name or IP address of the database server.
            graphname (str): The name of the graph to use.
            username (str): The user name for authentication.
            password (str): The password for authentication.
            restppPort (int): The port number of the REST++ API.
            gsPort (int): The port number of the GSQL API.
            apiToken (str): The API token for authentication.
            secret (str): The secret for authentication.
            useCert (bool): Whether to use SSL certificate or not.
        """
        self.host = host
        self.graphname = graphname
        self.username = username
        self.password = password
        self.secret = secret
        self.conn = tg.TigerGraphConnection(host=self.host, graphname=self.graphname, username=self.username, password=self.password)
        self.conn.getToken(self.secret)

    def create_node(self, id: str) -> bool:
        """Create a vertex with given id
        Args:
            id (str): the vertex id
        """
        return bool(self.conn.upsertVertex('user', id))

    def create_edge(self, source: str, target: str, interaction: str) -> bool:
        """Create an edge between two nodes in the database.

        Args:
            source (int): The ID of the source node.
            target (int): The ID of the target node.
            interaction (str): The type of interaction between the nodes, such as MT, RE, or RT.
            create_nodes (bool, optional): Whether to create the source and target nodes if they do not exist. Defaults to False.

        Raises:
            requests.exceptions.HTTPError: If the request fails.
        """
        return bool(self.conn.upsertEdge(sourceVertexType="user",
                                         sourceVertexId=source,
                                         edgeType=interaction,
                                         targetVertexType="user",
                                         targetVertexId=target)

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()
    
    def __exit__(self):
        self.close()
