from neuron import h
import numpy as np
import matplotlib.pyplot as plt
from claustrum.claustrum_cell import ClaustrumCell

# Load compiled cell mechanisms
h.nrn_load_dll(r"C:\nrn\FYP_nrn\claustrum\claustrum channels\nrnmech.dll")
h.nrn_load_dll(r"C:\nrn\FYP_nrn\PFC\PFC channels\nrnmech.dll")

ps_factor = 1.75
threshold = 0

# Define a function to count spikes
def count_spikes(voltage_vec, threshold):
    spikes = 0
    above_threshold = False
    for voltage in voltage_vec:
        if voltage >= threshold and not above_threshold:
            spikes += 1
            above_threshold = True
        elif voltage < threshold:
            above_threshold = False
    return spikes

# Create claustrum cell
claustrum_cell = ClaustrumCell(ps_factor)

# Create PFC cells
h.load_file("C:/nrn/FYP_nrn/PFC/pfc_pc_temp_mod.hoc")
h.load_file("C:/nrn/FYP_nrn/PFC/incell.hoc")

pfc_cell = h.Pcell(ps_factor)
in_cell = h.INcell(ps_factor)

# Connection weights
pfc_to_cl_weight = 0.011 # set
cl_to_pfc_weight = 10**45 # set
cl_to_in_weight = 0.3 # set
pfc_to_in_weight = 0.3 # set
in_to_pfc_weight = 10**6 # set

# Connect PFC cells to Claustral Neuron - done
# nc_ampa = h.NetCon(pfc_cell.axon(0.5)._ref_v, claustrum_cell.ampa_soma, sec=pfc_cell.axon)
# nc_ampa.weight[0] = pfc_to_cl_weight

# Connect Claustral Neuron to PFC cells - done
# nc_to_pfc_ampa = h.NetCon(claustrum_cell.soma(0.5)._ref_v, pfc_cell.syn_ampa, sec=claustrum_cell.soma)
# nc_to_pfc_ampa.weight[0] = cl_to_pfc_weight

# Connect Claustral Neuron to IN cells - done
# nc_to_in_ampa = h.NetCon(claustrum_cell.soma(0.5)._ref_v, in_cell.syn_ampa, sec=claustrum_cell.soma)
# nc_to_in_ampa.weight[0] = cl_to_in_weight

# Connect PFC cells to IN cells - done
nc_pfc_to_in_ampa = h.NetCon(pfc_cell.soma(0.5)._ref_v, in_cell.syn_ampa, sec=pfc_cell.soma)
nc_pfc_to_in_ampa.weight[0] = pfc_to_in_weight

# # Connect IN cells to PFC cells - done
# nc_in_to_pfc_gabaa = h.NetCon(in_cell.soma(0.5)._ref_v, pfc_cell.syn_gabaa, sec=in_cell.soma)
# nc_in_to_pfc_gabaa.weight[0] = in_to_pfc_weight

# Set up a stimulation to test the connectivity
stim = h.IClamp(pfc_cell.soma(0.5))
stim.delay = 100
stim.dur = 3000
stim.amp = 0.3

# Record membrane potential of the Claustral Neuron
v_vec_claustral = h.Vector()
t_vec = h.Vector()
v_vec_pfc = h.Vector()
v_vec_in = h.Vector()

t_vec.record(h._ref_t)
#v_vec_claustral.record(claustrum_cell.soma(0.5)._ref_v)
v_vec_pfc.record(pfc_cell.soma(0.5)._ref_v)
v_vec_in.record(in_cell.soma(0.5)._ref_v)

# Run the simulation
h.finitialize(-70)
h.continuerun(3200)

# Count spikes for each cell type
#num_claustral_spikes = count_spikes(v_vec_claustral, threshold)
num_pfc_spikes = count_spikes(v_vec_pfc, threshold)
num_in_spikes = count_spikes(v_vec_in, threshold)

# Plot the results
plt.figure()
#plt.plot(t_vec, v_vec_claustral, color='blue', label=f'Claustral Neuron, ({num_claustral_spikes} spikes)')
plt.plot(t_vec, v_vec_pfc, color='darkorange', label=f'PYR Cell, ({num_pfc_spikes} spikes)')
plt.plot(t_vec, v_vec_in, color='mediumorchid', label=f'IN Cell, ({num_in_spikes} spikes)')
plt.xlabel('Time (ms)')
plt.ylabel('Membrane potential (mV)')
plt.legend()
plt.title(f'Functional connectivity testing, psychedelic scaling factor = {ps_factor}')
plt.show()






# # Create a synapse on the pfc neuron
# syn = h.ExpSyn(pfc_cell.dend[2](0.5))
# syn.tau = 2  # decay time constant
# syn.e = 0    # reversal potential

# # Create a NetCon object to connect claustral neuron spike output to the synapse
# netcon = h.NetCon(claustrum_cell.soma(0.5)._ref_v, syn)
# netcon.threshold = threshold  # threshold for spike detection in mV
# netcon.weight[0] = 0.2  # synaptic weight

# # Create a stimulus for the claustral neuron
# stim = h.IClamp(claustrum_cell.soma(0.5))
# stim.delay = 100  # start of stimulation in ms
# stim.dur = 3000    # duration of stimulation in ms
# stim.amp = 0.3   # amplitude of stimulation in nA

# # Record the membrane potentials
# t_vec = h.Vector().record(h._ref_t)
# v_vec_cl = h.Vector().record(claustrum_cell.soma(0.5)._ref_v)
# v_vec_pfc = h.Vector().record(pfc_cell.soma(0.5)._ref_v)

# # Run the simulation
# h.finitialize(-70)
# h.continuerun(3200)

# t = np.array(t_vec)
# v_claustrum = np.array(v_vec_cl)
# v_pyramidal = np.array(v_vec_pfc)

# # Detect spikes: find where the membrane potential crosses the threshold from below
# cl_spike_indices = np.where((v_claustrum[:-1] < threshold) & (v_claustrum[1:] >= threshold))[0]
# cl_num_spikes = len(cl_spike_indices)
# pfc_spike_indices = np.where((v_pyramidal[:-1] < threshold) & (v_pyramidal[1:] >= threshold))[0]
# pfc_num_spikes = len(pfc_spike_indices)

# # Plot the recorded membrane potentials
# plt.figure(1)
# plt.subplot(2, 1, 1)
# plt.plot(t, v_claustrum, label='Claustral Neuron')
# plt.text(0.9, 0.6, f'{cl_num_spikes} spikes')
# plt.legend()

# plt.subplot(2, 1, 2)
# plt.plot(t, v_pyramidal, label='Layer 5 Pyramidal Neuron')
# plt.text(0.9, 0.6, f'{pfc_num_spikes} spikes')
# plt.legend()

# plt.xlabel('Time (ms)')
# plt.ylabel('Membrane Potential (mV)')
# plt.show()

# # Calculate cross-correlation between the two signals

# # Normalize the signals
# # v_claustrum_norm = (np.array(v_claustrum) - np.mean(v_claustrum)) / np.std(v_claustrum)
# # v_pyramidal_norm = (np.array(v_pyramidal) - np.mean(v_pyramidal)) / np.std(v_pyramidal)

# # # Compute the cross-correlation
# # cross_corr = np.correlate(v_claustrum_norm, v_pyramidal_norm, mode='full')
# # lags = np.arange(-len(v_claustrum_norm) + 1, len(v_claustrum_norm))

# # # Plot the cross-correlation
# # plt.figure(2)
# # plt.plot(lags, cross_corr)
# # plt.xlabel('Lags')
# # plt.ylabel('Cross-correlation')
# # plt.title('Cross-correlation between Claustral and Pyramidal Neurons')
# # plt.show()

