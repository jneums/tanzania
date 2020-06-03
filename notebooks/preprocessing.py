#Here will be our strategy to handle gps_height:
# In fit() just save the input data as a data frame \
# with gps_height, lat, long, and gps_height > 0
# In transform(), if gps_height == 0, then 
# start at 0.1 radius, and check if there are any non-zero gps_instances.
# If yes, get the average, else, increment search radius 
# by 0.3 (0.1 increase corresponds to 11km approximately)
# If nothing is found within an increment of 2, then just ignore.
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd
import math

class GPSHeightImputer(BaseEstimator, TransformerMixin):
    def __init__(self,init_radius=0.1,increment_radius=0.3,method = 'custom'): 
        self.column_names = [] 
        self.init_radius = init_radius
        self.increment_radius = increment_radius
        self.method = method

    
    def __get_subset_records(self, latitude, longitude, df, radius):
        latitude_from = latitude - radius
        latitude_to = latitude + radius
        longitude_from = longitude - radius
        longitude_to = longitude + radius
        
        df_temp = df[(df['latitude'] >= latitude_from) & (df['latitude'] <= latitude_to) & 
                  (df['longitude'] >= longitude_from) & (df['longitude'] <= longitude_to)]
        return df_temp
       

    def fit(self, X, y=None):
        if self.method == 'custom':
            X['gps_height'] = X['gps_height'].astype(float)
            X['latitude'] = X['latitude'].astype(float)
            X['longitude'] = X['longitude'].astype(float)
            self.df = X[X['gps_height'] != 0]
        elif self.method == 'median':
            X['gps_height'] = X['gps_height'].astype(float)
            #X['gps_height'] = X['gps_height'].fillna(0)
            self.median = np.median(list(X[X['gps_height'] != 0]['gps_height']))

            if math.isnan(self.median):
                self.median = 0
        elif self.method == 'mean':
            X['gps_height'] = X['gps_height'].astype(float)
            #X['gps_height'] = X['gps_height'].fillna(0)
            self.mean = np.mean(list(X[X['gps_height'] != 0]['gps_height']))
            if math.isnan(self.mean):
                self.mean = 0

        self.column_names = X.columns
        return self
        
    def transform(self,X):
        if self.method == 'custom':
            X['gps_height'] = X['gps_height'].astype(float)
            X['latitude'] = X['latitude'].astype(float)
            X['longitude'] = X['longitude'].astype(float)
            gps_height_transformed = []
            for latitude, longitude, gps_height in \
                zip(X['latitude'],X['longitude'],X['gps_height']):
                radius = self.init_radius
                if gps_height == 0:
                    gps_height_temp = gps_height
                    while gps_height_temp == 0 and radius <= 2:
                        df_temp = self.__get_subset_records\
                                  (latitude,longitude,self.df,radius)

                        gps_height_temp = np.mean(df_temp[df_temp['gps_height']!=0]\
                                                  ['gps_height'])
                        if math.isnan(gps_height_temp):
                            gps_height_temp = 0 
                        radius = self.increment_radius + radius
                else:
                    gps_height_temp = gps_height
                gps_height_transformed.append(gps_height_temp)
            X['gps_height'] = gps_height_transformed
            #self.column_names = list(X.columns)
        elif self.method == 'median':
            gps_height = np.array(list(X['gps_height']))
            gps_height[gps_height == 0] = self.median
            #self.column_names = list(X.columns)
            #return X[['latitude','longitude','gps_height']]
            X['gps_height'] = gps_height
        elif self.method == 'mean':
            gps_height = np.array(list(X['gps_height']))
            gps_height[gps_height == 0] = self.mean
            #self.column_names = list(X.columns)
            #return X[['latitude','longitude','gps_height']]
            X['gps_height'] = gps_height

        self.column_names = X.columns
        X['gps_height'] = X['gps_height'].astype(float)
        X['gps_height'] = X['gps_height'].fillna(0)
        return X

#Here will be our strategy to handle gps_height:
# In fit() just save the input data as a data frame \
# with gps_height, lat, long, and gps_height > 0
# In transform(), if gps_height == 0, then 
# start at 0.1 radius, and check if there are any non-zero gps_instances.
# If yes, get the average, else, increment search radius 
# by 0.3 (0.1 increase corresponds to 11km approximately)
# If nothing is found within an increment of 2, then just ignore.

class LatLongImputer(BaseEstimator, TransformerMixin):
    def __init__(self, init_radius=0.1,increment_radius=0.3, method='custom'):
        self.column_names = []
        self.init_radius = init_radius
        self.increment_radius = increment_radius
        self.method = method
        self.df = pd.DataFrame()
        pass
    
    def __get_subset_records(self, latitude, longitude, df, radius):
        latitude_from = latitude - radius
        latitude_to = latitude + radius
        longitude_from = longitude - radius
        longitude_to = longitude + radius
        
        df_temp = df[(df['latitude'] >= latitude_from) & (df['latitude'] <= latitude_to) & \
                  (df['longitude'] >= longitude_from) & (df['longitude'] <= longitude_to)]
        return df_temp
    
    def fit(self, X, y=None):
        if self.method == 'mean':
            # find mean of all non-zero values
            self.mean_lat = np.mean(X[X['latitude'] != -2e-08]['latitude'])
            self.mean_long = np.mean(X[X['longitude'] != 0]['longitude'])
        elif self.method == 'median':
            # find median of all non-zero values
            self.median_lat = np.median(X[X['latitude'] != -2e-08]['latitude'])
            self.median_long = np.median(X[X['longitude'] != 0]['longitude'])
        elif self.method == 'custom':
            self.df['latitude'] = X[X['latitude'] != -2e-08]['latitude'] 
            self.df['longitude'] = X[X['longitude'] != 0]['longitude']
        self.column_names = ['latitude', 'longitude', 'gps_height']
        return self
    
    def transform(self, X):
        if self.method == 'mean':
            X['latitude'].replace(-2e-08, self.mean_lat, inplace=True)
            X['longitude'].replace(0, self.mean_long, inplace=True)
        elif self.method == 'median':
            X['latitude'].replace(-2e-08, self.median_lat, inplace=True)
            X['longitude'].replace(0, self.median_long, inplace=True)
        elif self.method == 'custom':
            lat_transformed = []
            long_transformed = []
            for latitude, longitude in zip(X['latitude'],X['longitude']):
                radius = self.init_radius
                if (latitude == -2e-08) | (longitude == 0):
                    lat_temp = latitude
                    long_temp = longitude
                    while lat_temp == -2e-08 and long_temp == 0 and radius <= 2:
                        df_temp = self.__get_subset_records(latitude,longitude,self.df,radius)
                        
                        lat_temp = np.mean(df_temp[df_temp['latitude']!=-2e-08]['latitude'])                        
                        long_temp = np.mean(df_temp[df_temp['longitude']!=0]['longitude'])

                        radius = self.increment_radius + radius
                else:
                    lat_temp = latitude
                    long_temp = longitude
                lat_transformed.append(lat_temp)
                long_transformed.append(long_temp)
            X['latitude'] = lat_transformed
            X['longitude'] = long_transformed
        self.column_names = X.columns
        return X

# will work the same way as the gps imputer. 
class PopulationImputer(BaseEstimator, TransformerMixin):
    def __init__(self, method='custom'):
        self.columns_names = []
        self.method = method
        self.df = pd.DataFrame()
        
    def fit(self, X, y=None):
        if self.method == 'mean':
            self.mean = np.mean(X[X['population'] > 0]['population'])
        elif self.method == 'median':
            self.median = np.median(X[X['population'] > 0]['population'])
        elif self.method == 'custom':
            self.df['population'] = X[X['population'] > 0]['population']
        
        self.column_names = ['latitude', 'longitude', 'population']
        return self
    
    def transform(self, X):
        X.fillna(0, inplace=True)
        if self.method == 'mean':
            X['population'].replace(0, self.mean, inplace=True)
        elif self.method == 'median':
            X['population'].replace(0, self.median, inplace=True)
        elif self.method == 'custom':
            pass
        self.column_names = ['latitude', 'longitude', 'population']
        return X[['latitude', 'longitude', 'population']]

class ConstructionYearTransformer(BaseEstimator, TransformerMixin):
    def __init__(self,method = 'custom'): 
        self.column_names = [] 
        #self.init_radius = init_radius
        #self.increment_radius = increment_radius
        self.method = method
        pass ##Nothing else to do
        
    def fit(self, X, y=None):
        X['construction_year'] = X['construction_year'].astype(float)
        if self.method == 'custom':
            year_recorded = X[X['construction_year'] > 0]\
                            ['date_recorded'].\
                            apply(lambda x: int(x.split("-")[0]))
            year_constructed = X[X['construction_year'] > 0]['construction_year']
            self.median_age = np.median(year_recorded - year_constructed)
            self.column_names = ['age']
            return self
        if self.method == 'median':
               X['construction_year'] = X['construction_year'].astype(float)
               #X['gps_height'] = X['gps_height'].fillna(0)
               self.median = \
                          np.median(list(X[X['construction_year'] != 0]['construction_year']))
               if math.isnan(self.median):
                  self.median = 0
               self.column_names = ['construction_year']
               return self
        if self.method == 'mean':
               X['construction_year'] = X['construction_year'].astype(float)
               #X['gps_height'] = X['gps_height'].fillna(0)
               self.mean = np.mean(list(X[X['construction_year'] != 0]['construction_year']))
               if math.isnan(self.mean):
                  self.mean = 0
               self.column_names = ['construction_year']
               return self

        if self.method == 'ignore':
               self.column_names = ['construction_year']
               return self
          
    def transform(self,X):
        if self.method == 'custom':
            year_recorded = list(X['date_recorded'].apply(lambda x: int(x.split("-")[0])))
            year_constructed = list(X['construction_year'])
            age = []
            for i,j in enumerate(year_constructed):
                if j == 0:
                   age.append(self.median_age)
                else:
                   temp_age = year_recorded[i] - year_constructed[i]
                   if temp_age < 0:
                      temp_age = self.median_age
                   age.append(temp_age)   
            X['age'] = age
            self.column_names = ['age']
            #self.column_names = X.columns
            return X[['age']]
        if self.method == 'median':      
                X['construction_year'] = X['construction_year'].astype(float)
                X['construction_year'] = X['construction_year'].fillna(0)
                construction_year = np.array(list(X['construction_year']))
                construction_year[construction_year == 0] = self.median
                self.column_names = ['construction_year']
                X['construction_year'] = construction_year
                return X[['construction_year']]

        if self.method == 'mean':
                X['construction_year'] = X['construction_year'].astype(float)
                X['construction_year'] = X['construction_year'].fillna(0)
                construction_year = np.array(list(X['construction_year']))
                construction_year[construction_year == 0] = self.mean
                self.column_names = ['construction_year']
                X['construction_year'] = construction_year
                return X[['construction_year']]
        
        if self.method == 'ignore':      
                X['construction_year'] = X['construction_year'].astype(float)
                X['construction_year'] = X['construction_year'].fillna(0)
                self.column_names = ['construction_year']
                return X[['construction_year']]       

# take columns and turn them into 3 numerical columns representing percent of target
class HighCardTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.column_names = []
        self.df = pd.DataFrame()
        self.mean_map = {}
        pass

    def fit(self, X, y=None):
        X = pd.concat([X, y], axis=1)
        self.target_col = y.name
        dummies_status = pd.get_dummies(X[self.target_col])
        dummies_status.columns = [ f"{self.target_col}_{column_name}" for column_name in dummies_status.columns.tolist()]
        self.dummies = dummies_status.columns
        X = X.join(dummies_status)
        
        for target in self.dummies:
            self.mean_map[target] = {}
            for col in X.columns:
                for val in X[col].unique():
                    mean = np.mean(X[X[col] == val][target])
                    if np.isnan(mean):
                        mean = 0
                    self.mean_map[target][val] = self.mean_map.get(
                        val, mean)
        self.column_names = X.columns
        return self

    def transform(self, X):
        for feature_name in X.columns:
            for target_col in self.dummies:
                X[feature_name+'_'+target_col[-1:]] = X[feature_name].map(self.mean_map[target_col])
            X = X.drop(feature_name, axis=1)
        self.column_names = X.columns
        return X

# Takes 'region' and 'district_code' and combines them together
class DistrictCodeMerge(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.column_names = []
        pass
    
    def fit(self, X, y=None):
        self.column_names = ['district']
        return self

    def transform(self, X):
        X['district'] = X['region'] + ', ' + X['district_code'].astype(str)
        self.column_names = ['district']
        return X[['district']]

# Take in 'extraction_type', 'extraction_type_group', 'extraction_type_class' and flatten them
class ExtractionMerge(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.column_names = []
        pass
    
    def __unique(self, sequence):
        seen = set()
        return [x for x in sequence if not (x in seen or seen.add(x))]
    
    def __merge(self, x):
        x = x.split(',')
        x = self.__unique(x)
        return ":".join(x)
    
    def fit(self, X, y=None):
        self.column_names = ['extraction']
        return self
    
    def transform(self, X):
        X['extraction'] = X['extraction_type_class'] + ',' + X['extraction_type_group'] + ',' + X['extraction_type']
        X['extraction'] = X['extraction'].apply(self.__merge)
        self.column_names = ['extraction']
        return X[self.column_names]