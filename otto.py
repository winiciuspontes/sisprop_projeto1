import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class Otto:
    def __init__(self, **kwargs):
        
        # Constantes
        self.R = 287
        self.gamma = 1.4
        
        # Inputs
        self.combustivel = kwargs['combustivel']
        self.p1 = kwargs['p1']
        self.t1 = kwargs['t1']
        self.cr = kwargs['cr']
        self.N = kwargs['rpm'] / 60
        self.proporcao_mistura = kwargs['proporcao_mistura']
        self.vh = kwargs['vh']
        self.cv = kwargs['cv']
        self.cp = kwargs['cp']
        self.qh = kwargs['calor_reacao']
        self.mf = kwargs['mf']
        self.altitude = kwargs["altitude"]
        
        # Calcula os estados 1, 2, 3, 4
        self.calcula_estados()

    def calcula_estados(self):
        self.estado1()
        self.estado2()
        self.estado3()
        self.estado4()
        
        return print("Estados calculados com sucesso")  
    
    
    def estado1(self):
        self.v1 = ((self.R * self.t1) / self.p1)
    
    def estado2(self):
        self.t2 = ((self.cr) ** (self.gamma - 1)) * self.t1
        self.v2 = self.v1 / self.cr
        self.p2 = ((self.v1 / self.v2) ** self.gamma) * self.p1
    
    def estado3(self):
        self.t3 = self.t2 + (self.qh / self.cv)
        self.p3 = (self.t3 / self.t2) * self.p2
    
    def estado4(self):
        self.t4 = ((1 / (self.cr)) ** (self.gamma - 1)) * self.t3
        self.v3 = self.v2
        self.v4 = self.v3 * self.cr
        self.p4 = ((self.v3 / self.v4 ) ** self.gamma ) * self.p3
    
    def eficiencia_termica(self):
        self.eficiencia_term = 1 - ((1 / self.cr) ** (self.gamma - 1))
        return self.eficiencia_term
    
    def pressa_media_efet(self):
        self.ql = self.cv * (self.t4 - self.t1)
        self.w_net = self.qh - self.ql
        self.mep = self.w_net / (self.v1 - self.v2)
        return self.mep

    def calcula_pot_eixo(self):
        mep = self.pressa_media_efet()
        self.pot_eixo = mep * self.vh * (self.N / 2)
        return self.pot_eixo
    
    def consumo_especifico(self):
        pot = self.calcula_pot_eixo()
        self.consumo_esp = self.mf / pot
        return self.consumo_esp
        
    
    
    def resumo(self):
        estados_dados = {
            'Estado': ['Estado 1', 'Estado 2', 'Estado 3', 'Estado 4'],
            'Pressão (Pa)': [self.p1, self.p2, self.p3, self.p4],
            'Temperatura (K)': [self.t1, self.t2, self.t3, self.t4],
            'Volume (m³)': [self.v1, self.v2, self.v3, self.v4]
        }
        
        estados_df = pd.DataFrame(estados_dados)
        
        eficiencia_dados = {
            'Combustível': [self.combustivel],
            'Eficiência Térmica %': [self.eficiencia_termica()],
            'MEP (KPa)': [self.pressa_media_efet()],
            'Potência no Eixo (W)': [self.calcula_pot_eixo()],
            'Consumo Especifico': [self.consumo_especifico()]
        }
        
        eficiencia_df = pd.DataFrame(eficiencia_dados)
        
        return estados_df, eficiencia_df
    
