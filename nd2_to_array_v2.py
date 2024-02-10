# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:08:07 2021

@author: Alexandros Papagiannakis, Christine Jacobs-Wagner lab, Sarafan ChEM-H, Stanford University 2021
"""


import numpy as np
from pims import ND2_Reader


def nd2_to_array(images_path):
    """
    This function is used to convert .nd2 images to numpy arrays.
    It also returms the image metadata.
    
    Parameters
    ----------
    image_path - string: the path of the .nd2 file

    Returns
    -------
    [0] the iteration axis - string ('c', 't', 'mc' or 'mct')
    [1] the .nd2 metadata and images (from the ND2_Reader pims module). This is a class object and has multuiple functions
    [2] a dictionary which contains the images as numpy arrays organized by:
        iteration_axis 't' - For fast time lapse (stream acquisition), key2: frame
        iteration_axis 'c' - For snapshots of a single XY position, key1: channel
        iteration_axis 'mc' - For snapshots of multiple XY positions, key1: position, key2: channel
        iteration_axis = 'mct' - For time lapse across different channels, key1: position, key2: channel, key3: time-point
    [3] channels: list of strings - each string represents the channel (e.g. ['Phase', 'mCherry', 'GFP', 'Phase_after'])
        If a certain wavelength (lambda) is used two times in the ND acquisition, then the second channel instance is referred to as '_after'
        An empty list is returned if no channels are selected.
    [4] the number of time-points - positive integer or zero if the Time label was not selected in the ND acquisition
    [5] The number of XY positions - positive integer or zero if the XY label was not selected in the ND acquisition
    [6] The scale of the image - float: microns per pixel
    [7] THe dimensions of the image - tuple: (x,y) dimensions of the camera sensor or the ROI
    
    Notes
    -----
    This function was adapted to include all possible channel, time-point, xy-position permutations in our image acquisition protocols in NIS elements (including the JOBS module)
    New permutations may need to be included.
    The iteration axis determines how the image dimensions are iterated and stored into dictionaries. Some NIS elements version may use 'm' for the xy position and other versions use 'v'.
    The current version of the code uses iteration axes that include 'm'. Update if the NIS elements software uses 'v' for xy position iterations. 
    """
    # The path of the .nd2 file 
    images = ND2_Reader(images_path)
    # "C:\Users\Alex\Anaconda3\Lib\site-packages\pims_nd2\nd2reader.py"
    # This path has been modified in lines 228 and 229 to accommodate the function.
    #print('metadata:',images.metadata)
    print('dimensions:',images.sizes)
    
    scale = round(images.metadata['calibration_um'],3)  # μm/px scale
    sensor = (images.sizes['x'], images.sizes['y'])
    channels = []
    if 'c' in images.sizes:
        # get the channels and frames from the .nd2 metadata
        number_of_channels = images.sizes['c']
        
        for i in range(number_of_channels):
            ch = images.metadata['plane_'+str(i)]['name']
            if ch in channels:
                channels.append(ch+'_after')
            else:
                channels.append(ch)   
    # number_of_frames = images.metadata['sequence_count']
    iteration_axis = ''
    if 'v' in images.sizes and images.sizes['v'] > 1:
        iteration_axis += 'm'
        number_of_positions = images.sizes['v']
    if 'm' in images.sizes and images.sizes['m'] > 1:
        iteration_axis += 'm'
        number_of_positions = images.sizes['m']
    if 'c' in images.sizes and images.sizes['c'] > 1:
        iteration_axis += 'c'
    if 't' in images.sizes and images.sizes['t'] > 1:
        iteration_axis += 't'
        number_of_timepoints = images.sizes['t']
    
    print(iteration_axis)
    # For a stream acquisition
    if iteration_axis == 't':
        image_arrays = {}
        number_of_positions = 0
        with images as frames:
            t = 0 # time point
            print(frames)
            frames.iter_axes = iteration_axis
            for frame in frames:
                image_arrays[t] = np.array(frame)
                t += 1
        frames.close()
    # For snapshots at different channels
    elif iteration_axis == 'c':
        image_arrays = {}
        number_of_timepoints = 0
        number_of_positions = 0
        with images as frames:
            i = 0
            print(frames)
            frames.iter_axes = iteration_axis
            for frame in frames:
                image_arrays[channels[i]] = np.array(frame)
                i += 1
        frames.close()
    # For snapshots at different XY positions for a single channel (this is how JOBS extracts the snapshots)
    elif iteration_axis == 'm':      
        image_arrays = {}
        number_of_timepoints = 0
        number_of_channels = 1
        with images as frames:
            i = 0
            print(frames)
            frames.iter_axes = iteration_axis
            for frame in frames:
                image_arrays[i] = np.array(frame)
                i += 1
        frames.close()
    # For snapshots at different channels and XY positions
    elif iteration_axis == 'mc':
        image_arrays = {}
        number_of_timepoints = 0
        with images as frames:
            print(frames)
            frames.iter_axes = iteration_axis
            pos = 0
            ch = 0
            image_arrays[pos] = {}
            for frame in frames:
                if ch < number_of_channels:
                    if pos < number_of_positions:
                        image_arrays[pos][channels[ch]] = np.array(frame)
                        ch+=1
                elif ch == number_of_channels:
                    pos += 1
                    image_arrays[pos] = {}
                    ch = 0
                    image_arrays[pos][channels[ch]] = np.array(frame)
                    ch+=1
        frames.close()
    # For snapshots at different channels and XY positions and timepoints
    elif iteration_axis == 'mt':
        image_arrays = {}
        with images as frames:
            print(frames)
            frames.iter_axes = iteration_axis
            pos = 0
            tm = 0
            image_arrays[pos] = {}
            for frame in frames:
                if tm < number_of_timepoints:
                    image_arrays[pos][tm] = np.array(frame)
                    tm+=1
                elif tm == number_of_timepoints:
                    tm = 0
                    if pos < number_of_positions-1:
                        pos += 1
                        image_arrays[pos] = {}
                        image_arrays[pos][tm] = np.array(frame)
                        tm+=1             
        frames.close()
    # For snapshots at different channels and XY positions and timepoints
    elif iteration_axis == 'mct':
        image_arrays = {}
        with images as frames:
            print(frames)
            frames.iter_axes = iteration_axis
            pos = 0
            ch = 0
            tm = 0
            image_arrays[pos] = {}
            image_arrays[pos][channels[ch]] = {}
            for frame in frames:
                if tm < number_of_timepoints:
                    image_arrays[pos][channels[ch]][tm] = np.array(frame)
                    tm+=1
                elif tm == number_of_timepoints:
                    tm = 0
                    if ch < number_of_channels-1:
                        ch += 1
                        image_arrays[pos][channels[ch]] = {}
                        image_arrays[pos][channels[ch]][tm] = np.array(frame)
                        tm+=1
                    elif ch == number_of_channels-1:
                        ch = 0
                        pos+=1
                        image_arrays[pos] = {}
                        image_arrays[pos][channels[ch]] = {}
                        image_arrays[pos][channels[ch]][tm] = np.array(frame)
                        tm+=1
        frames.close()
        
        
    elif iteration_axis == 'ct':
        image_arrays = {}
        with images as frames:
            print(frames)
            frames.iter_axes = iteration_axis
            ch = 0
            tm = 0
            image_arrays[channels[ch]] = {}
            for frame in frames:
                if tm < number_of_timepoints:
                    image_arrays[channels[ch]][tm] = np.array(frame)
                    tm+=1
                elif tm == number_of_timepoints:
                    tm = 0
                    if ch < number_of_channels-1:
                        ch += 1
                        image_arrays[channels[ch]] = {}
                        image_arrays[channels[ch]][tm] = np.array(frame)
                        tm+=1             
        frames.close()
    
    # if no channels or time points are specified there should be only one image
    elif iteration_axis == '':
        number_of_timepoints = 0
        number_of_positions = 0
        with images as frames:
            for frame in frames:
                image_arrays = np.array(frame)
    
    return iteration_axis, images, image_arrays, channels, number_of_timepoints, number_of_positions, scale, sensor
