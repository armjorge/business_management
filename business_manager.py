import os
import sys

class BusinessManager:
    def __init__(self, folder_root):
        self.folder_root = folder_root
        self._load_business_module()
    
    def _load_business_module(self):
        """Carga el módulo de business management existente"""
        try:
            # Importar el módulo original
            from .business_management import business_management
            self.business_management = business_management
        except ImportError as e:
            print(f"⚠️ No se pudo cargar el módulo de business: {e}")
            self.business_management = None
    
    def run_business_menu(self):
        """Ejecuta el menú de business management"""
        if self.business_management:
            self.business_management(self.folder_root)
        else:
            print("❌ Módulo de business no disponible")