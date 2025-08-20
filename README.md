# business_management

# 📌 Nombre del proyecto

## 🧠 Resumen
Sistema automatizado para la gestión de flujos de caja empresariales que permite crear, validar y consolidar presupuestos de ingresos y egresos. Genera reportes financieros acumulativos para facilitar la toma de decisiones y el control presupuestario.

## ❗ Problema
La gestión manual de presupuestos empresariales es propensa a errores, consume mucho tiempo y dificulta el seguimiento en tiempo real del flujo de caja. Los archivos dispersos de ingresos y egresos hacen complejo obtener una visión consolidada de la situación financiera.

## ✅ Solución
Este sistema automatiza la creación de archivos presupuestales estandarizados, valida automáticamente los datos financieros y genera reportes consolidados de flujo de caja con análisis acumulativo, proporcionando una visión clara y actualizada de la salud financiera empresarial.

## ⚙️ ¿Qué hace este script?
- [x] Crea archivos Excel estandarizados para registro de ingresos y egresos
- [x] Valida automáticamente fechas y montos en los archivos presupuestales
- [x] Asigna códigos únicos a cada renglón presupuestal para trazabilidad
- [x] Consolida múltiples archivos de ingresos y egresos en un reporte unificado
- [x] Genera flujo de caja acumulativo con balance diario
- [x] Crea reportes detallados en Excel con hojas separadas para análisis y desglose

## 🛠️ Estructura del repositorio

```
business_management/
├── business_management.py          # Script principal
├── README.md                      # Documentación
└── Implementación/               # Carpeta de trabajo (generada automáticamente)
    └── Presupuesto/             # Directorio de archivos presupuestales
        ├── Ingresos/            # Archivos Excel de ingresos
        ├── Egresos/             # Archivos Excel de egresos
        └── Presupuesto.xlsx     # Reporte consolidado final
```

## 🔧 Funcionalidades Técnicas

### Creación de Archivos Presupuestales
El sistema genera archivos Excel con estructura estandarizada:
- **Columnas**: fecha dd mm yyyy, Concepto, [Ingresos/Egresos], Código Renglón
- **Validación automática** de tipos de datos (fechas y montos numéricos)
- **Códigos únicos** por renglón para trazabilidad

### Procesamiento y Validación
- **Lectura automática** de todos los archivos .xlsx en carpetas de Ingresos y Egresos
- **Validación de estructura** de columnas antes del procesamiento
- **Filtrado de datos** - solo procesa filas con fechas y montos válidos
- **Asignación de códigos** únicos por archivo y renglón

### Generación de Reportes
- **Consolidación** de múltiples archivos en un DataFrame unificado
- **Agrupación por fecha** con suma de ingresos y egresos
- **Cálculo de balance diario** (Ingresos - Egresos)
- **Flujo acumulativo** para seguimiento de tendencias
- **Exportación a Excel** con hojas separadas:
  - "Flujo de caja": Resumen acumulativo por fecha
  - "Desglose": Detalle completo de todas las transacciones

## 🔐 Configuración del archivo YAML

El sistema puede extenderse con configuración YAML para credenciales o parámetros adicionales:

```yaml
# Configuración futura para integraciones
api_key: "clave_api_bancaria"
directorio_backup: "/ruta/respaldos"
formato_fecha: "dd/mm/yyyy"
moneda_base: "MXN"
```

## 🚀 Modo de Uso

1. **Ejecutar el script**: `python business_management.py`
2. **Elegir opción**:
   - Opción 1: Crear nuevos archivos de ingresos/egresos
   - Opción 2: Generar reporte consolidado de flujo de caja
3. **Seguir las instrucciones** interactivas en pantalla
4. **Revisar resultados** en la carpeta `Implementación/Presupuesto/`

