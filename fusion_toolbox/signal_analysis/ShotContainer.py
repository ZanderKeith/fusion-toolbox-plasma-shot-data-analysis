

class ShotContainer():
    """Holds data for a single shot number from multiple sources.
    """

    def __init__(self, device, shot_number):
        """Initialize an empty shot container for a given shot number on a specified device.

        Args:
            device (str): name of the device that took the shot
            shot_number (int): the shot number

        Returns:
            ShotContainer: A container for the shot data
        """

        self.device = device
        self.shot_number = shot_number
        self.data_dict = {}

    def add_data(self, data, source_name):
        """Add shot data from a source to the container.

        Args:
            data (Pandas.DataFrame): Pandas Dataframe containing the time-series data for the shot
            source_name (str): Name of data source (ex: SQL, MDSPlus, Disruption-Py)
        """

        self.data_dict[source_name] = data

    def get_data(self, source_name):
        """Get the data for a given source.

        Args:
            source_name (str): Name of data source (ex: SQL, MDSPlus, Disruption-Py)

        Returns:
            Pandas.DataFrame: Pandas Dataframe containing the time-series data for the shot
        """

        return self.data_dict[source_name]