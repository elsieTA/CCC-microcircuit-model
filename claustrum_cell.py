# claustrum_cell.py
from neuron import h
import math

h.load_file("stdrun.hoc")

class ClaustrumCell():
    name = "ClaustrumCell"

    def __init__(self, ps_factor=1):
        self.ps_factor = ps_factor
        self._setup_morphology()
        self._setup_biophysics()
        self._setup_synapses()

    def _setup_morphology(self):
        # Create the cell topology
        self.soma = h.Section(name='soma', cell=self)
        self.hillock = h.Section(name='hillock', cell=self)
        self.iseg = h.Section(name='iseg', cell=self)
        self.axon = h.Section(name='axon', cell=self)
        self.dend1 = h.Section(name='dend1', cell=self)
        self.dend2 = h.Section(name='dend2', cell=self)

        self.hillock.connect(self.soma)
        self.iseg.connect(self.hillock)
        self.axon.connect(self.iseg)
        self.dend1.connect(self.soma)
        self.dend2.connect(self.dend1)

        # Set geometry
        self.soma.diam = 26.08
        self.hillock.diam = 2.79
        self.iseg.diam = 1.72
        self.axon.diam = 1.5
        self.dend1.diam = 2.58
        self.dend2.diam = 1.51

        self.hillock.L = 7.49
        self.iseg.L = 13.14
        self.axon.L = 700
        self.dend1.L = 100
        self.dend2.L  = 600

    def _setup_biophysics(self):
        # Set passive properties
        self.soma.Ra = 135.77
        self.hillock.Ra = 132.46
        self.iseg.Ra = 182.09
        self.axon.Ra = 126.26
        self.dend1.Ra = 228.11
        self.dend2.Ra = 505.344

        for sec in self.allsec():
            sec.insert(h.pas)
            sec(0.5).pas.g = 0.0000173
            sec(0.5).pas.e = -74.5
            sec.cm = 0.729

        # Insert ion channels
        self.ih_list = h.SectionList()
        self.nat_list = h.SectionList()
        self.kfast_list = h.SectionList()
        self.kslow_list = h.SectionList()
        self.dendtree_list = h.SectionList()

        self.ih_list.append(self.dend1)
        self.ih_list.append(self.dend2)

        self.nat_list.append(self.soma)
        self.nat_list.append(self.hillock)
        self.nat_list.append(self.iseg)
        self.nat_list.append(self.dend1)
        self.nat_list.append(self.dend2)

        self.kfast_list.append(self.soma)
        self.kfast_list.append(self.dend1)
        self.kfast_list.append(self.dend2)

        self.kslow_list.append(self.soma)
        self.kslow_list.append(self.dend1)
        self.kslow_list.append(self.dend2)

        self.dendtree_list.append(self.dend1)
        self.dendtree_list.append(self.dend2)

        for sec in self.ih_list:
            sec.insert('ih_c')

        for sec in self.nat_list:
            sec.insert('nat_c')
            sec.ena = 55

        h.nat_c.vshift = 10

        for sec in self.kfast_list:
            sec.insert('kfast_c')
            sec.ek = -80

        for sec in self.kslow_list:
            sec.insert('kslow_c')
            sec.ek = -80

        self.soma.insert('nap_c')
        self.soma.insert('km_c')
        #self.soma.ek = -58

        self.dend2.insert('sca_c')
        self.dend2.insert('kca_c')
        self.dend2.insert('cad_c')
        self.dend2.eca = 140

        # Set channel distribution parameters
        self.soma(0.5).nat_c.gbar = 486.12
        self.soma(0.5).kfast_c.gbar = 75.72 * self.ps_factor
        self.soma(0.5).kslow_c.gbar = 281.81 * self.ps_factor
        self.soma(0.5).nap_c.gbar = 0.34
        self.soma(0.5).km_c.gbar = 8.33 * self.ps_factor
        self.dend2(0.5).ih_c.gbar = 131.78
        self.dend2(0.5).nat_c.gbar = 59.84
        self.hillock(0.5).nat_c.gbar = 17477.89
        self.iseg(0.5).nat_c.gbar = 7918.13
        self.iseg(0.5).nat_c.vshift2 = -2.04
        self.dend2(0.5).sca_c.gbar = 1.31
        self.dend2(0.5).sca_c.vshift = 9.24
        self.dend2(0.5).kca_c.gbar = 0.98

        dendscaling = 0.75

        lambda_Kfast = 38.45
        lambda_Kslow = 35.53

        self.dend2(0.5).pas.g = self.soma(0.5).pas.g * dendscaling
        self.dend2.cm = self.soma.cm * dendscaling

        dend_distance = h.distance(self.dend1(0), self.dend2(1))

        # Exponential decay
        for sec in self.dendtree_list:
            for seg in sec:
                seg_x = seg.x * dend_distance
                seg.kfast_c.gbar = self.soma(0.5).kfast_c.gbar * math.exp(-seg_x / lambda_Kfast)
                seg.kslow_c.gbar = self.soma(0.5).kslow_c.gbar * math.exp(-seg_x / lambda_Kslow)

        # Linear decay
        self.dend2_mih = self.dend2(0.5).ih_c.gbar / dend_distance
        self.dend2_mnat = (self.dend2(0.5).nat_c.gbar - self.soma(0.5).nat_c.gbar) / dend_distance

        for seg in self.dend1:
            seg_x = seg.x * self.dend1.L
            seg.ih_c.gbar = self.dend2_mih * seg_x
            seg.nat_c.gbar = (self.dend2_mnat * seg_x) + self.soma(0.5).nat_c.gbar

    def _setup_synapses(self):
        self.ampa_soma = h.ExpSyn(self.soma(0.5))
        self.ampa_soma.tau = 5

        self.netcons_to_cells = []  # Store NetCons for connections from claustral neuron to other cells

    def allsec(self):
        return [self.soma, self.hillock, self.iseg, self.axon, self.dend1, self.dend2]
