'''data_transformations.py
Maya Purohit
Performs translation, scaling, and rotation transformations on data
CS 251: Data Analysis and Visualization
Fall 2023

NOTE: All functions should be implemented from scratch without loops using basic NumPy — no high-level library calls.
'''
import numpy as np


def normalize(data):
    '''Perform min-max normalization of each variable in a dataset.

    Parameters:
    -----------
    data: ndarray. shape=(N, M). The dataset to be normalized.

    Returns:
    -----------
    ndarray. shape=(N, M). The min-max normalized dataset.
    '''

    data = (data - data.min(axis = 0)) / (data.max(axis = 0) - data.min(axis = 0)) #normalize by substracting the min and divding be the extent 

    return data #return the numpy array
    


def center(data):
    '''Center the dataset.

    Parameters:
    -----------
    data: ndarray. shape=(N, M). The dataset to be centered.

    Returns:
    -----------
    ndarray. shape=(N, M). The centered dataset.
    '''

    data = data - data.mean(axis = 0) #center by substracting by the mean of each column

    return data
    


def rotation_matrix_3d(degrees, axis='x'):
    '''Make a 3D rotation matrix for rotating the dataset about ONE variable ("axis").

    Parameters:
    -----------
    degrees: float. Angle (in degrees) by which the dataset should be rotated.
    axis: str. Specifies the variable about which the dataset should be rotated. Assumed to be either 'x', 'y', or 'z'.

    Returns:
    -----------
    ndarray. shape=(3, 3). The 3D rotation matrix.

    NOTE: This method just CREATES and RETURNS the rotation matrix. It does NOT actually PERFORM the rotation!
    '''

    # find the degree angle in radians
    theta = np.deg2rad(degrees)

    if axis == "x": #makes the rotation matrix depending on the axis we want to rotate around 
        rotationMat = np.array([[1,0,0],
                                [0,np.cos(theta), -np.sin(theta)],
                                [0,np.sin(theta), np.cos(theta)]])
    elif axis == "z":
        rotationMat = np.array([[np.cos(theta), -np.sin(theta),0],
                                [np.sin(theta), np.cos(theta),0],
                                [0,0,1]])
    else:
        rotationMat = np.array([[np.cos(theta),0, np.sin(theta)],
                                [0,1,0],
                                [-np.sin(theta), 0, np.cos(theta)]
                                ])

    return rotationMat

    
