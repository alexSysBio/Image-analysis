This repository includes useful functions for the analysis of microscopy images:

nd2_to_array:
  The nd2_to_array function can be used to import .nd2 files into python. The files are stored into a dictionary which includes elemenets of the iteration axis as   keys and the image 2D numpy arrays as values. It uses the nd2 image reader from the pims library:
  https://pypi.org/project/pims-nd2/#:~:text=pims_nd2%20contains%20a%20reader%20for,and%20nice%20display%20in%20IPython.
  
  I have tested most of the implemented iterations from microscopy images I have acquired. If the remaining iterations do not work it should be an easy fix. Please reach out if any exceptions pop up.

  Cite:
    https://www.biorxiv.org/content/10.1101/2024.10.08.617237v2.full
    
    DNA/polysome phase separation and cell width confinement couple nucleoid segregation 
    to cell growth in Escherichia coli
    
    Alexandros Papagiannakis, Qiwei Yu, Sander K. Govers, Wei-Hsiang Lin,  Ned S. Wingreen, Christine Jacobs-Wagner
    
    bioRxiv, https://doi.org/10.1101/2024.10.08.617237, October 22, 2024



Biviriate_medial_axis_estimation:
  The function get_medial_axis draws the central line of elongated (rod-shaped) cells from pole to pole. A set to test the medial axis estimation is also provided along with a notebook that demonstrates how the function works. The get_oned_coordinates function projects all the cell pixels onto the central line,
  in relative or absolute arch-length coordinates from pole to pole. The distance from the central line is multiplied by the sign of the cross product to get the 
  orientation of the cell pixels around the medial axis (above or below). An example for implementing the medial axis estimation is provided in the test_medial_axis.ipynb notebook.

  Cite:
    https://www.biorxiv.org/content/10.1101/2024.10.08.617237v2.full
    
    DNA/polysome phase separation and cell width confinement couple nucleoid segregation 
    to cell growth in Escherichia coli
    
    Alexandros Papagiannakis, Qiwei Yu, Sander K. Govers, Wei-Hsiang Lin,  Ned S. Wingreen, Christine Jacobs-Wagner
    
    bioRxiv, https://doi.org/10.1101/2024.10.08.617237, October 22, 2024
  


  Background_correction:
    This scripts includes the functions required for a cell-free background estimation and subtraction. This is a fast implementation where a the cell-free background is calculated within square image sectors (tiles). These squared regions have a side which is a perfect divisor of the image dimensions. An alternative implementation, which is however slower, would involve a rolling window with a step of 1-pixel. An example for implementing background correction is provided in the test_background_correction.ipynb notebook.

  Cite:
    https://www.biorxiv.org/content/10.1101/2024.10.08.617237v2.full
    
    DNA/polysome phase separation and cell width confinement couple nucleoid segregation 
    to cell growth in Escherichia coli
    
    Alexandros Papagiannakis, Qiwei Yu, Sander K. Govers, Wei-Hsiang Lin,  Ned S. Wingreen, Christine Jacobs-Wagner
    
    bioRxiv, https://doi.org/10.1101/2024.10.08.617237, October 22, 2024


Omnipose to python:
    This is a class that can be used to incorporate the cell lineages traced by Omnipose and SupperSegger into Python.
    <br> Omnipose: https://www.nature.com/articles/s41592-022-01639-4
    <br> SuperSegger: https://pubmed.ncbi.nlm.nih.gov/27569113/
    <br> see also: https://www.biorxiv.org/content/10.1101/2024.11.25.625259v1.full

    The class can be initialized running the following function:
      omnipose_to_python_timelapse(omni_cell_path, experiment, fluorescent_channels, min_trajectory_length, frame_interval, every_nth, save_path)
    Other functions incldued in the class:
      get_cell_out_of_boundaries(limits)
      get_mothers_without_daughters()
      get_medial_axes(bad_cells, verb=False)
      locate_cell_id(cell_position, frame, radius)
      get_lineage_mother(single_cell_id)
      get_oned_fluorescence(single_cell_id)

  Cite:
    https://www.biorxiv.org/content/10.1101/2024.10.08.617237v2.full
    
    DNA/polysome phase separation and cell width confinement couple nucleoid segregation 
    to cell growth in Escherichia coli
    
    Alexandros Papagiannakis, Qiwei Yu, Sander K. Govers, Wei-Hsiang Lin,  Ned S. Wingreen, Christine Jacobs-Wagner
    
    bioRxiv, https://doi.org/10.1101/2024.10.08.617237, October 22, 2024


