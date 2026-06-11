# claustrum_stimulation.py
from neuron import h
import numpy as np
import matplotlib.pyplot as plt
from claustrum.claustrum_cell import ClaustrumCell

# Load compiled cell mechanisms
h.nrn_load_dll(r"C:\nrn\FYP_nrn\claustrum\claustrum channels\nrnmech.dll")

# Define the ps_factor values
ps_factors = [1, 1.25, 1.5, 1.75, 2]
stim_amps = [0.1, 0.2, 0.3, 0.4, 0.5]

fig, axs = plt.subplots(len(ps_factors), len(stim_amps), figsize=(20, 15), sharex=True, sharey=True)

for row, ps_factor in enumerate(ps_factors):
    claustrum_cell = ClaustrumCell(ps_factor)

    all_t = []
    all_v = []
    num_spikes_list = []

    for amp in stim_amps:
        stim = h.IClamp(claustrum_cell.soma(0.5))
        stim.delay = 100
        stim.dur = 3000
        stim.amp = amp

        t_vec = h.Vector().record(h._ref_t)
        v_vec = h.Vector().record(claustrum_cell.soma(0.5)._ref_v)

        h.finitialize(-70)
        h.continuerun(3500)

        t = np.array(t_vec)
        v = np.array(v_vec)

        all_t.append(t)
        all_v.append(v)

        threshold = 0
        spike_indices = np.where((v[:-1] < threshold) & (v[1:] >= threshold))[0]
        num_spikes = len(spike_indices)

        num_spikes_list.append(num_spikes)

    for col, amp in enumerate(stim_amps):
        axs[row, col].plot(all_t[col], all_v[col], label=f'amp={amp} nA, ps={ps_factor}')
        axs[row, col].legend(loc='upper right')
        textstr = f'{num_spikes_list[col]} spikes'
        axs[row, col].text(0.99, 0.6, textstr, transform=axs[row, col].transAxes,
                           fontsize=12, verticalalignment='bottom', horizontalalignment='right',
                           bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))

# for ax in axs[-1, :]:
#     ax.set_xlabel('Time (ms)')
# fig.text(0.02, 0.5, 'Membrane Potential (mV)', va='center', rotation='vertical', fontsize=12)
# fig.suptitle('Claustral neuron response for various K+ conductance scaling factors')
plt.tight_layout(rect=[0.02, 0.03, 1, 0.95])
plt.show()
