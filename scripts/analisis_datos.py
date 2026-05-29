import os
import pandas as pd
import matplotlib.pyplot as plt

def ejecutar_analisis_ventas():
    # 1. REPRODUCIBILIDAD Y RUTAS RELATIVAS
    # Definimos las rutas relativas basadas en la estructura obligatoria del repositorio
    ruta_datos = os.path.join("..", "datos", "dataset.csv")
    ruta_grafico = os.path.join("..", "resultados", "grafico_resultados.png")
    
    print("Iniciando el procesamiento de datos de ventas...")

    # 2. IMPORTAR LOS DATOS
    # Intentamos cargar el archivo CSV ubicado en la carpeta /datos
    try:
        # Se asume que el dataset tiene las columnas obligatorias: id, sales_date, sales_amount, producto, cantidad
        df = pd.read_csv(ruta_datos)
        print("¡Dataset cargado correctamente!")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {ruta_datos}.")
        print("Asegurate de haber guardado el CSV en la carpeta /datos con el nombre 'dataset.csv'.")
        return

    # Convertimos la columna de fecha a tipo datetime para poder agrupar por mes correctamente
    df['sales_date'] = pd.to_datetime(df['sales_date'])
    
    # Si el dataset no tiene 'sales_amount' pero tiene 'precio' y 'cantidad vendida', la calculamos:
    if 'sales_amount' not in df.columns and 'precio' in df.columns and 'cantidad_vendida' in df.columns:
        df['sales_amount'] = df['precio'] * df['cantidad_vendida']

    # 3. CÁLCULO DE INDICADORES REQUERIDOS
    print("\n--- CALCULANDO INDICADORES EMPRESARIALES ---")
    
    # Indicador A: Ventas Totales (Suma de todo el monto de ventas)
    ventas_totales = df['sales_amount'].sum()
    print(f"Ventas Totales de la Empresa: ${ventas_totales:,.2f}")
    
    # Indicador B: Producto más vendido (Agrupamos por producto y sumamos cantidades)
    # Nota: Si tu dataset usa la columna 'producto' y 'cantidad_vendida'
    if 'producto' in df.columns and 'cantidad_vendida' in df.columns:
        producto_mas_vendido = df.groupby('producto')['cantidad_vendida'].sum().idxmax()
        cantidad_maxima = df.groupby('producto')['cantidad_vendida'].sum().max()
        print(f"Producto más vendido: {producto_mas_vendido} ({cantidad_maxima} unidades)")
    else:
        # Alternativa por monto si cambian los nombres de columnas
        producto_mas_vendido = df.groupby('id')['sales_amount'].sum().idxmax()
        print(f"ID de Transacción con mayor venta: {producto_mas_vendido}")

    # Indicador C: Ventas por mes (Agrupamos por año-mes y sumamos el monto)
    df['mes'] = df['sales_date'].dt.to_period('M')
    ventas_por_mes = df.groupby('mes')['sales_amount'].sum()
    print("\nEvolución de ventas mensuales:")
    print(ventas_por_mes.to_string())

    # 4. GENERACIÓN DEL GRÁFICO DE EVOLUCIÓN
    print("\nGenerando gráfico de evolución temporal...")
    
    plt.figure(figsize=(10, 5))
    # Convertimos el índice de períodos a string para que Matplotlib lo grafique sin problemas
    ventas_por_mes.plot(kind='line', marker='o', color='darkblue', linewidth=2)
    
    # Configuración estética y etiquetas profesionales
    plt.title("Evolución Mensual de Ventas Comerciales", fontsize=14, fontweight='bold')
    plt.xlabel("Período (Mes)", fontsize=11)
    plt.ylabel("Monto Total de Ventas ($)", fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout() # Evita que se corten las etiquetas al guardar
    
    # 5. GUARDAR RESULTADOS EN LA CARPETA CORRESPONDIENTE
    # Guardamos el gráfico de manera automática en /resultados
    plt.savefig(ruta_grafico)
    plt.close()
    print(f"¡Gráfico guardado exitosamente en: {ruta_grafico}!")
    
    # Opcional: Exportar un mini informe de texto con los indicadores calculados
    ruta_informe = os.path.join("..", "resultados", "indicadores_clave.txt")
    with open(ruta_informe, "w") as f:
        f.write("RESUMEN DE DESEMPEÑO COMERCIAL\n")
        f.write("==============================\n")
        f.write(f"Ventas Totales: ${ventas_totales:,.2f}\n")
        if 'producto' in df.columns:
            f.write(f"Producto Estrella: {producto_mas_vendido}\n")
        f.write("\nDetalle de Ventas Mensuales:\n")
        f.write(ventas_por_mes.to_string())
    print(f"¡Informe de indicadores guardado en: {ruta_informe}!")

if __name__ == "__main__":
    ejecutar_analisis_ventas()