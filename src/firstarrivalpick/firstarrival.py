from scipy.io import wavfile
from scipy.signal import butter, lfilter, hilbert
import matplotlib.pyplot as plt
import numpy as np

# Define the range and construct file paths for 30Hz and 50Hz
file_numbers = list(range(1, 29))  # From 1 to 30
file_paths_30 = [f"bedrock_hjemme_10_2024/hjem_{num}m_30.wav" for num in file_numbers]
file_paths_50 = [f"bedrock_hjemme_10_2024/hjem_{num}m_50.wav" for num in file_numbers]

# Define a function to read and process data
def read_and_process(file_paths):
    data_dict = {}
    for num, path in zip(file_numbers, file_paths):
        samplerate, data = wavfile.read(path, mmap=False)
        if data.ndim > 1:
            data = data[:, 0]
        data_dict[f"data{num}m"] = data
    min_length = min(data.shape[0] for data in data_dict.values())
    for key in data_dict.keys():
        data_dict[key] = data_dict[key][:min_length]
    no_samples = min_length
    duration = no_samples / samplerate
    t = np.arange(0, duration, 1/samplerate)
    return data_dict, samplerate, t

# Process data for both 30Hz and 50Hz
data_dict_30, samplerate_30, t_30 = read_and_process(file_paths_30)
data_dict_50, samplerate_50, t_50 = read_and_process(file_paths_50)

# Define the Butterworth filter function
def design_filter(Fcutoff, Fs, Order=2):
    return butter(Order, Fcutoff / (Fs / 2), btype='low')

# Function to apply the filter
def apply_filter(data, b, a):
    return lfilter(b, a, data)

# Calculate envelope
def calculate_envelope(data):
    analytic_signal = hilbert(data)
    envelope = np.abs(analytic_signal)
    return envelope

# Function to detect the first break
def detect_first_break(envelope, threshold):
    first_break_index = np.argmax(envelope > threshold)
    return first_break_index

# Filter data for both 30Hz and 50Hz
b_30, a_30 = design_filter(30, samplerate_30)
data_filt_dict_30 = {key: apply_filter(data, b_30, a_30) for key, data in data_dict_30.items()}
data_filt_dict_30 = {key: data / np.max(np.abs(data)) * 3 for key, data in data_filt_dict_30.items()}

b_50, a_50 = design_filter(50, samplerate_50)
data_filt_dict_50 = {key: apply_filter(data, b_50, a_50) for key, data in data_dict_50.items()}
data_filt_dict_50 = {key: data / np.max(np.abs(data)) * 3 for key, data in data_filt_dict_50.items()}

# Unique colors and styles for each plot
colors = [ 'red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple', 'brown', 
          'lime', 'pink', 'grey', 'turquoise', 'olive', 'navy', 'teal', 'maroon', 'aqua', 'fuchsia', 
          'gold', 'indigo', 'violet', 'lavender', 'beige', 'salmon', 'coral', 'chocolate', 'tan', 'peru']
labels = [f'{num}m' for num in file_numbers]
threshold = 0.1  # Threshold for detecting the first break

# Plotting 30Hz data in the first window
plt.figure(figsize=(12, 6))
for i, (key, color, label) in enumerate(zip(data_filt_dict_30.keys(), colors, labels)):
    filtered_data = data_filt_dict_30[key]
    envelope = calculate_envelope(filtered_data)
    first_break_index = detect_first_break(envelope, threshold)
    first_break_time = first_break_index / samplerate_30
    plt.plot(t_30, filtered_data + (i + 1), color=color, label=label)
    plt.axvline(x=first_break_time, color='r', linestyle='--')
plt.xlabel('Time')
plt.ylabel('Normalized Amplitude')
plt.title('Traces Plot - 30Hz with First Breaks')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show(block=False)  # Non-blocking show

# Plotting 50Hz data in the second window
plt.figure(figsize=(12, 6))
for i, (key, color, label) in enumerate(zip(data_filt_dict_50.keys(), colors, labels)):
    filtered_data = data_filt_dict_50[key]
    envelope = calculate_envelope(filtered_data)
    first_break_index = detect_first_break(envelope, threshold)
    first_break_time = first_break_index / samplerate_50
    plt.plot(t_50, filtered_data + (i + 1), color=color, label=label)
    plt.axvline(x=first_break_time, color='r', linestyle='--')
plt.xlabel('Time')
plt.ylabel('Normalized Amplitude')
plt.title('Traces Plot - 50Hz with First Breaks')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show(block=False)  # Non-blocking show

# Keep the plots open
input("Press Enter to close the plots...")
