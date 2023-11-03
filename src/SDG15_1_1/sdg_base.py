from typing import List, Optional, Union 
from collections.abc import Callable
from abc import ABC, abstractmethod
import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import glob
import os
from tqdm import tqdm


class SDGBase(ABC):   
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes
    ----------
    attr1 : str
        Description of `attr1`.
    attr2 : :obj:`int`, optional
        Description of `attr2`.

    """
    
    def __init__(self, root_in_dir: str, root_out_dir: Optional[str] = None) -> None:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        self.set_root_in_dir(root_in_dir)
        
        if root_out_dir is not None:
            self.set_output_dir(root_out_dir)
        else:
            self.set_output_dir(root_in_dir)          

        
    def set_root_in_dir(self, root_in_dir: str) -> None:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        self._root_in_dir = root_in_dir
        self.create_folders(self._root_in_dir)

        
    def get_root_in_dir(self) -> str:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        return self._root_in_dir

    
    def set_output_dir(self, root_out_dir: str) -> None:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        self._output_dir = f'{root_out_dir}/'
        self.create_folders(self._output_dir)

        
    def get_output_dir(self) -> str:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        return self._output_dir

    
    def create_folders(self, new_dir: str) -> bool:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        try:
            os.makedirs(new_dir, exist_ok=True)
            print(f'Directory {new_dir} was created or already existed')
        except Exception as e:
            print(f'Unable to make directory {new_dir} because of error {e}')
        
        
    def get_ext_files(self, inp_folder: str, ext: str, search_string: Optional[str] = None) -> List[str]:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        all_files = glob.glob(f'{self.get_root_in_dir()}/{inp_folder}/*.{ext}')
        if search_string:
            all_files = [f for f in all_files if search_string in f]
        return all_files
    
    
    def _get_read_function(self, ext: str) -> Callable:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        data_read_dict = {
            'csv' : pd.read_csv,
            'shp' : gpd.read_file,
            'xlsx': pd.read_excel,
        }    
        return data_read_dict[ext]
    
    
    def load_data(self, file_path: str, cols: List[str] = None, index: str = None, epsg: int = 27700) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        ext = file_path.split('.')[-1]
        read_func = self._get_read_function(ext)
        df = read_func(file_path)
        df.columns = df.columns.str.lower()
        if cols:
            df = df[cols]
        if index:
            df = df.set_index(index)
        if isinstance(df, gpd.GeoDataFrame) and not df.crs.to_epsg() == epsg:
            df = df.to_crs(epsg)
            df = df.set_geometry(df['geometry'])

        return df   

    
    def save_data(self, file: Union[pd.DataFrame, gpd.GeoDataFrame], file_name: str) -> bool:
        """__summary__

        Parameters
        ----------
        param1: type
            The first parameter.
        param2: type
            The second parameter.

        Returns
        -------
        bool
            __returns__

        """
        if isinstance(file, pd.DataFrame):
            file.to_csv(f'{self.get_output_dir()}{file_name}.csv')
        if isinstance(file, gpd.GeoDataFrame):
            file.to_file(f'{self.get_output_dir()}{file_name}.shp')
        return True
    
    
    @abstractmethod
    def calculate_sdg(self):
        pass
    