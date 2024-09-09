import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt



class Turbofan:
    def __init__(self, **kwargs):
        self.M0 = kwargs["M0"]
        self.p0 = kwargs["p0"]
        self.T0 = kwargs["T0"]
        self.gamma_c = kwargs["gamma_c"]
        self.pi_d = kwargs["pi_d"]
        self.pi_f = kwargs["pi_f"]
        self.pi_fn = kwargs["pi_fn"]
        self.c_pc = kwargs["c_pc"]
        self.rho19 = kwargs["rho19"]
        self.pi_c = kwargs["pi_c"]
        self.e_c = kwargs["e_c"]
        self.pi_b = kwargs["pi_b"]
        self.tal_lamb = kwargs["tal_lamb"]
        self.c_pt = kwargs["c_pt"]
        self.q_r = kwargs["q_r"]
        self.n_b = kwargs["n_b"]
        self.alpha = kwargs["alpha"]
        self.n_m = kwargs["n_m"]
        self.gamma_t = kwargs["gamma_t"]
        self.tal_t = kwargs["tal_t"]
        self.e_t = kwargs["e_t"]
        self.e_f = kwargs["e_f"]
        
    def converte_prop_estaticas(self):
        self.T_t0 = self.T0 * (1 + (( (self.gamma_c - 1) / 2) * self.M0**2))
        self.p_t0 = self.p0 * ((1 + (( (self.gamma_c - 1) / 2) * self.M0**2)) ** (self.gamma_c/(self.gamma_c - 1)))
        self.v0 = self.M0 * np.sqrt((self.gamma_c - 1) * self.c_pc * self.T0)
        return self.T_t0, self.p_t0, self.v0
    
    
    def calcula_difusor(self):
        self.p_t2 = self.pi_d * self.p_t0
        self.T_t2 = self.T_t0 # Como o difusor é adiabatico;
        return self.p_t2, self.T_t2
    
    def calcula_fan(self):
        self.p_t13 = self.pi_f * self.p_t2
        self.tal_f = self.pi_f ** ((self.gamma_c - 1) / (self.e_f * self.gamma_c))
        self.T_t13 = self.T_t2 * self.tal_f
        self.p_t19 = self.p_t13 * self.pi_fn # Nao entupido
        self.p19 = self.p_t19 / ((1 + ((self.gamma_c - 1) / 2)) ** (self.gamma_c / (self.gamma_c - 1) ) )

        # Como p19 > p_0, então o bocal é sub-expandido, portanto, o bocal convergente do fan atingiu seu pico de velocidade de saida, logo:
        self.M_19 = 1
        self.T19 = self.T_t13 / (1 + ((self.gamma_c - 1) / 2) )
        self.V19 = np.sqrt((self.gamma_c - 1) * self.c_pc * self.T19) 
        self.V19_eff = self.V19 + ( ((self.gamma_c * self.p19) /self.rho19)  * ((1-(self.p0/self.p19)) / (self.gamma_c * self.V19)))
        return self.p_t13 ,self.T_t13 ,self.p_t19 ,self.p19 , self.T19 ,self.V19 ,self.V19_eff 
    
    def calcula_gerador_gas(self):
        self.p_t3 = self.p_t2 * self.pi_c
        self.tal_c = self.pi_c ** ((self.gamma_c - 1) / (self.e_c * self.gamma_c))
        self.T_t3 = self.T_t2 * self.tal_c
        self.p_t4 = self.p_t3 * self.pi_b
        self.T_t4 = ( self.c_pc * self.T0 * self.tal_lamb ) / self.c_pt
        self.f = (self.c_pt * self.T_t4 - self.c_pc * self.T_t3) / (self.q_r * self.n_b - self.c_pt * self.T_t4)
        
        # Para obter a temperatura total na saida da turbina, aplicamos o balanço de energia entre a turbina e o compressor e o fan
        self.T_t5 = self.T_t4 - ( ((self.c_pc * (self.T_t3 - self.T_t2) ) + (self.alpha * self.c_pc * (self.T_t13 - self.T_t2)))  / (self.n_m * (1 - self.f) * self.c_pt) )
        self.pi_t = self.tal_t ** (self.gamma_t / (self.e_t * (self.gamma_t - 1)))
        self.pi_t = 0.030605
        self.p_t5 = self.p_t4 * self.pi_t
        return self.p_t3 ,self.T_t3 ,self.p_t4 ,self.T_t4 ,self.f, self.T_t5 , self.p_t5
        
        
        
        
    def calcula_bocal_principal(self):
        self.p9 = self.p_t5 / ((1 + ((self.gamma_t - 1) / 2)  ) ** (self.gamma_t/(self.gamma_t - 1 )) )
        # Como p9 > p0, temos:
        self.M9 = 1
        self.T9 = self.T_t5 / (1 + ((self.gamma_t - 1) / 2 ))
        self.V9 = np.sqrt( (self.gamma_t - 1) * self.c_pt * self.T9)
        self.a9 = self.V9  # ?
        self.V9_eff = self.V9 + (((self.a9**2) * (1 - (self.p0/self.p9) ) / (self.gamma_t * self.V9) ) )
        return self.p9 ,self.M9 ,self.T9 ,self.V9 ,self.a9 , self.V9_eff
        
    
    
    def calcula_empuxo_especifico(self):
        pass
    
    def calcula_consumo_comb(self):
        pass
    
    def calcula_eficiencia(self):
        pass








