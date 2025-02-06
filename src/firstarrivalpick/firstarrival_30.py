# pip install -U first-breaks-picking
# Installer Conda/Mini Conda
# conda install conda-forge::obspy

# Links
# https://github.com/DaloroAT/first_breaks_picking
# Travel times hjemme_10: https://github.com/stefanjetschny/bedrock/blob/main/data/bedrock_hjemme_10_2024/travel_times.xlsx
# Analyse av data hjemme_10: https://docs.google.com/spreadsheets/d/1nYwR3StzZGs_PDxQuTspGLBca1e5amLq/edit?gid=790628807#gid=790628807

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for rendering plots to files
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import obspy
from obspy.core import Stream, Trace
from obspy.io.segy.segy import SEGYBinaryFileHeader, SEGYTraceHeader
from first_breaks.sgy.reader import SGY
from first_breaks.picking.task import Task
from first_breaks.picking.picker_onnx import PickerONNX
from first_breaks.desktop.graph import export_image

# Define the range and construct file paths for 30Hz and 50Hz
file_numbers = range(1, 30)  # From 1 to 30
file_paths_30 = [f"/home/sjet/repos/bedrock/data/bedrock_hjemme_10_2024/hjem_{num}m_30.wav" for num in file_numbers]
# file_paths_50 = [f"/home/sjet/repos/bedrock/data/bedrock_hjemme_10_2024/hjem_{num}m_50.wav" for num in file_numbers]

# Define a function to read and process data
def read_and_process(file_paths):
    data_dict = {}
    for num, path in zip(file_numbers, file_paths):
        samplerate, data = wavfile.read(path, mmap=False)
        data = data[:, 0] if data.ndim > 1 else data
        data_dict[f"data{num}m"] = data
    return data_dict, samplerate

data_dict_30, samplerate_30 = read_and_process(file_paths_30)
# data_dict_50, samplerate_50 = read_and_process(file_paths_50)

# Define the Butterworth filter function and apply the filter
def filter_data(data_dict, cutoff, samplerate, order=2):
    b, a = butter(order, cutoff / (samplerate / 2), btype='low')
    return {key: lfilter(b, a, data) / np.max(np.abs(lfilter(b, a, data))) * 3 for key, data in data_dict.items()}

data_filt_dict_30 = filter_data(data_dict_30, 30, samplerate_30)
# data_filt_dict_50 = filter_data(data_dict_50, 50, samplerate_50)

# Convert filtered data to SEG-Y format using ObsPy
def convert_to_segy(data_dict, samplerate, filename, min_samples, max_samples=32767):
    traces = []
    for i, (key, data) in enumerate(data_dict.items()):
        trace_data = data[min_samples:max_samples].astype(np.float32)  # Limit trace length to max_samples
        trace = Trace(data=trace_data)
        trace.stats.sampling_rate = samplerate
        trace.stats.starttime = obspy.UTCDateTime(0)
        trace.stats.segy = {}
        trace.stats.segy.trace_header = SEGYTraceHeader()
        trace.stats.segy.trace_header.trace_sequence_number_within_line = i + 1
        traces.append(trace)
    stream = Stream(traces=traces)
    
    # Set SEG-Y file headers
    binary_header = SEGYBinaryFileHeader()
    stream.binary_file_header = binary_header
    stream.textual_file_header = (
        b"C 1 CLIENT                        COMPANY  CREW NO         "
        b"C 2 LINE            AREA                        MAP ID      "
        b"C39 SEG Y REV1                                                      "
        b"C40 END TEXTUAL HEADER                                            "
    )

    stream.write(filename, format='SEGY', data_encoding=1)  # Use data_encoding=1 for float32

# Create a single SEG-Y file for 30Hz data
convert_to_segy(data_filt_dict_30, samplerate_30, "filtered_data_30.sgy", 1025)

# Create a single SEG-Y file for 50Hz data
# convert_to_segy(data_filt_dict_50, samplerate_50, "filtered_data_50.sgy")

print("Data has been converted to SEG-Y format.")

def process_segy_files(filenames):
    picker = PickerONNX()
    for filename in filenames:
        if os.path.exists(filename):
            print(f"Processing file: {filename}")
            try:
                sgy = SGY(filename)
                
                # Create a task for the picker
                task = Task(source=sgy, traces_per_gather=7, maximum_time=0, gain=2)
                
                # Process the task and pick the first break
                task = picker.process_task(task)
                
                picks = task.get_result()
                print(picks.picks_in_samples)
                
                # Set pick color
                task.picks.color = (255, 0, 0)
                
                # Export image using export_image function
                image_filename = f"{os.path.splitext(filename)[0]}.png"
                export_image(task, image_filename, show_processing_region=False,height=700, width=1500)
                print(f"Image saved as {image_filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")
        else:
            print(f"File not found: {filename}")

# Process the SEG-Y files for both frequencies
# process_segy_files(["filtered_data_30.sgy", "filtered_data_50.sgy"])
process_segy_files(["filtered_data_30.sgy"])
