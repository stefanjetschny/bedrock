from scipy.io import wavfile
from scipy.signal import butter, lfilter
import numpy as np
import obspy
from obspy.core import Stream, Trace
from obspy.io.segy.segy import SEGYBinaryFileHeader, SEGYTraceHeader
import os
from first_breaks.sgy.reader import SGY
from first_breaks.picking.task import Task
from first_breaks.picking.picker_onnx import PickerONNX

# Define the range and construct file paths for 30Hz and 50Hz
file_numbers = range(1, 30)  # From 1 to 29
file_paths_30 = [f"bedrock_hjemme_10_2024/hjem_{num}m_30.wav" for num in file_numbers]
file_paths_50 = [f"bedrock_hjemme_10_2024/hjem_{num}m_50.wav" for num in file_numbers]

# Define a function to read and process data
def read_and_process(file_paths):
    data_dict = {}
    for num, path in zip(file_numbers, file_paths):
        samplerate, data = wavfile.read(path, mmap=False)
        data = data[:, 0] if data.ndim > 1 else data
        data_dict[f"data{num}m"] = data
    return data_dict, samplerate

data_dict_30, samplerate_30 = read_and_process(file_paths_30)
data_dict_50, samplerate_50 = read_and_process(file_paths_50)

# Define the Butterworth filter function and apply the filter
def filter_data(data_dict, cutoff, samplerate, order=2):
    b, a = butter(order, cutoff / (samplerate / 2), btype='low')
    return {key: lfilter(b, a, data) / np.max(np.abs(lfilter(b, a, data))) * 3 for key, data in data_dict.items()}

data_filt_dict_30 = filter_data(data_dict_30, 30, samplerate_30)
data_filt_dict_50 = filter_data(data_dict_50, 50, samplerate_50)

# Convert filtered data to SEG-Y format using ObsPy
def convert_to_segy(data_dict, samplerate, filename, max_samples=32767):
    traces = []
    for i, (key, data) in enumerate(data_dict.items()):
        trace_data = data[:max_samples].astype(np.float32)  # Limit trace length to max_samples
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
convert_to_segy(data_filt_dict_30, samplerate_30, "filtered_data_30.sgy")

# Create a single SEG-Y file for 50Hz data
convert_to_segy(data_filt_dict_50, samplerate_50, "filtered_data_50.sgy")

print("Data has been converted to SEG-Y format.")

# Define the path to your SEG-Y file
segy_file = 'filtered_data_30.sgy'
# segy_file = 'real_gather.sgy'

# Read the SEG-Y file using ObsPy
stream = obspy.read(segy_file)

# To access individual traces and their headers
for i, trace in enumerate(stream):
    print(f"Trace {i + 1}:")
    print(trace)

from first_breaks.sgy.reader import SGY
from first_breaks.picking.task import Task
from first_breaks.picking.picker_onnx import PickerONNX
import os

def process_segy_files(filenames):
    picker = PickerONNX()
    for filename in filenames:
        if os.path.exists(filename):
            print(f"Processing file: {filename}")
            try:
                sgy = SGY(filename)
                
                # Create a task for the picker
                task = Task(source=sgy, traces_per_gather=12, maximum_time=100, gain=2)
                
                # Process the task and pick the first break
                task = picker.process_task(task)
                
                # Debug print to see picks
                print(f"Picks for {filename}: {task.picks}")
                
                # Print all picks
                pick_times = [pick for pick in task.picks]
                print(f"All picks for {filename}: {pick_times}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")
        else:
            print(f"File not found: {filename}")

# Process the SEG-Y files for both frequencies
process_segy_files(["filtered_data_30.sgy", "filtered_data_50.sgy"])
