# expands file size by a factor of 4.242
import os
import nibabel as nib
import time
# use all 4 cores in CPU for pandas
import pandas as pd
# Scans directory should contain only .nii.gz files
for file in os.listdir("./Scans"):
    if file.split(".")[1] == "nii" and not os.path.exists(file.split(".")[0] + ".csv"):
        img = nib.load('./Scans/' + file)
        data = img.get_fdata()
        print("opened " + file)
        # start timer
        start_time = time.time()
        # collect all time frames into a list of DataFrames
        time_series = []
        # iterate through times
        for t_cube in range(data.shape[3]):
            # collect all 147456 voxels in the cube into a 2D array
            cube_voxels = []
            # iterate through all 34 cross-sections of the cube
            for z_slice in range(data.shape[2]):
                # collect all 4096 voxels in the cross-section into a 1D array
                slice_voxels = []
                # iterate through all 64 lines in the cross-section
                for y_line in range(data.shape[1]):
                    # append all 64 voxels in the line to the collection
                    for x_voxel in range(data.shape[0]):
                        slice_voxels.append(data[x_voxel, y_line, z_slice, t_cube])
                cube_voxels.append(slice_voxels)
            # convert the 2D array to a DataFrame
            time_series.append(pd.DataFrame(cube_voxels))
        # concatenate the time series into a single DataFrame
        df = pd.concat(time_series)
        # save the whole time series DataFrame as a csv file
        df.to_csv(file.split(".")[0] + ".csv")
        execution_time = time.time() - start_time
        print("converted " + file + " in " + str(execution_time) + " seconds")
    else:
        pass
print("done")