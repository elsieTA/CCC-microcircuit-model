from neuron import h
import matplotlib.pyplot as plt
import numpy as np

h.load_file("stdrun.hoc")

# Load compiled cell mechanisms
h.nrn_load_dll(r"C:\nrn\FYP_nrn\PFC\PFC channels\nrnmech.dll")

# Load the HOC file
h.load_file("C:/nrn/FYP_nrn/PFC/incell.hoc")

ps_factor = 2

# Create an instance of the cell template defined in the HOC file
in_cell = h.INcell(ps_factor)

# Define the stimulation amplitudes
stim_amps = [0.1, 0.2, 0.3, 0.4, 0.5]

# Record membrane potential and time for each simulation
all_t = []
all_v = []
num_spikes_list = []

for amp in stim_amps:
    # Create a new current clamp stimulus for each amplitude
    stim = h.IClamp(in_cell.soma(0.5))
    stim.delay = 100  # start of stimulation in ms
    stim.dur = 3000     # duration of stimulation in ms
    stim.amp = amp    # amplitude of stimulation in nA

    # Record membrane potential and time
    t_vec = h.Vector().record(h._ref_t)
    v_vec = h.Vector().record(in_cell.soma(0.5)._ref_v)

    # Run the simulation
    h.finitialize(-70)
    h.continuerun(3500)

    # Convert recorded data to numpy arrays for easier processing
    t = np.array(t_vec)
    v = np.array(v_vec)

    # Store the results
    all_t.append(t)
    all_v.append(v)

    # Define the threshold for spike detection
    threshold = 0  # mV, adjust as needed for your specific neuron model

    # Detect spikes: find where the membrane potential crosses the threshold from below
    spike_indices = np.where((v[:-1] < threshold) & (v[1:] >= threshold))[0]
    num_spikes = len(spike_indices)

    # Store the number of spikes
    num_spikes_list.append(num_spikes)

# Plot the results
fig, axs = plt.subplots(len(stim_amps), 1, figsize=(10, 15), sharex=True, sharey=True)

for i, amp in enumerate(stim_amps):
    axs[i].plot(all_t[i], all_v[i], color='green') #, label=f'amp={amp} nA')
    axs[i].set_xticklabels([])
    axs[i].set_yticklabels([])
    #axs[i].set_ylabel('Membrane Potential (mV)', fontsize=8)
    # axs[i].legend(loc='upper right')
    # textstr = f'{num_spikes_list[i]} spikes'
    # axs[i].text(0.99, 0.6, textstr, transform=axs[i].transAxes,
    #             fontsize=12, verticalalignment='bottom', horizontalalignment='right',
    #             bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))

# axs[-1].set_xlabel('Time (ms)')
# # Set ylabel for the whole plot
# fig.text(0.02, 0.5, 'Membrane Potential (mV)', va='center', rotation='vertical', fontsize=12)
# fig.suptitle(f'PFC interneuron response, psychedelic effect scaling factor = {ps_factor}')
plt.tight_layout(rect=[0, 0, 1, 1])
plt.show()