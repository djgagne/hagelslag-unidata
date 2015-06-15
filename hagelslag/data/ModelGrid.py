from netCDF4 import Dataset
import numpy as np


class ModelGrid(object):
    """
    Base class for reading 2D model output grids from netCDF files.
    """
    def __init__(self, filenames):
        self.filenames = filenames
        self.file_objects = []

    def __enter__(self):
        """
        Open each file for reading.

        """
        for filename in self.filenames:
            try:
                self.file_objects.append(Dataset(filename))
            except RuntimeError:
                print("Warning: File {0} not found.".format(filename))
                self.file_objects.append(None)

    def load_data(self, variable):
        """
        Loads time series of 2D data grids from each opened file. The code 
        handles loading a full time series from one file or individual time steps
        from multiple files. Missing files are supported.

        :param variable: Name of the variable being loaded
        """
        if len(self.file_objects) == 1 and self.file_objects[0] is not None:
            data = self.file_objects[0].variables[variable][:]
        elif len(self.file_objects) > 1:
            grid_shape = [len(file_objects), 1, 1]
            for file_object in self.file_objects:
                if file_object is not None:
                    grid_shape = file_object.variables[variable].shape
                    break
            data = np.zeros((len(self.file_objects), grid_shape[1], grid_shape[2]))
            for f, file_object in self.file_objects:
                if file_object is not None:
                    data[f] = file_object.variables[variable][0]
        else:
            data = None
        return data

    def __exit__(self):
        """
        Close links to all open file objects and delete the objects.
        """
        for file_object in self.file_objects:
            file_object.close()
        del self.file_objects[:]

    def close(self):
        """
        Close links to all open file objects and delete the objects.
        """
        self.__exit__()
