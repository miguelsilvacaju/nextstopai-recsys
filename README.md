# 🌍 NextStop AI – Recommender System for Travel Packages

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)  
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-LightFM%2C%20PyTorch-orange)](https://pytorch.org/)  
[![ETL](https://img.shields.io/badge/ETL-SSIS%20%7C%20SQL%20Server%202022-green)](https://learn.microsoft.com/sql/integration-services)  
[![License](https://img.shields.io/badge/License-MIT-black)](LICENSE)

**Universidad de Ingeniería y Tecnología (UTEC)**  
📚 **Maestría en Ciencia de Datos – Proyecto Final**

NextStop AI es una **plataforma inteligente de marketing para turismo** que personaliza campañas de correo electrónico y recomendaciones de paquetes de viaje, incrementando la **conversión**, el **ticket promedio** y la **fidelización de clientes**.  

---

## 📌 Contexto y Oportunidad de Negocio

En la **Promotora de Turismo Nuevo Mundo**, las campañas actuales son **genéricas** (68k correos por campaña) y provocan pérdidas anuales de más de **$250,000 en conversiones no logradas**.  

👉 Según *Harvard Business Review*, un aumento del **5% en la retención de clientes** puede incrementar las ganancias entre **25% y 95%**.  

**Oportunidad Estratégica:**  
- Optimizar la conversión.  
- Fidelizar mediante experiencias personalizadas.  
- Aumentar la satisfacción de viajeros recurrentes.  

---

## 👥 Stakeholders y User Stories

### 🎯 Stakeholder Interno – Subgerente de Marketing
- **User Story**:  
  *Como Subgerente de Marketing, quiero una herramienta que recomiende los mejores paquetes de viaje para poder ejecutar campañas de email altamente personalizadas y aumentar la tasa de conversión.*  

- **Dolores**:  
  - Segmentación manual e ineficiente.  
  - Bajas tasas de apertura y conversión.  
  - Sin un sistema de recomendación claro para cada cliente.  

---

### 🧳 Stakeholder Externo – Viajero Recurrente
- **User Story**:  
  *Como Viajero recurrente, quiero recibir recomendaciones personalizadas de boletos y paquetes para ahorrar tiempo, acceder a mejores ofertas y disfrutar experiencias ajustadas a mis preferencias.*  

- **Dolores**:  
  - Recibe promociones irrelevantes.  
  - Percibe poco valor en las ofertas.  
  - Disminuye confianza y fidelidad hacia la marca.  

---

## 💡 Propuesta del Data Product

**NextStop AI** es un sistema de soporte a decisiones que optimiza campañas personalizadas para agencias de viajes.  

**Cómo funciona (3 pasos):**  
1. Analiza el historial de compras y viajeros similares.  
2. Predice destinos y ofertas con mayor probabilidad de interés.  
3. Personaliza y envía campañas de email adaptadas a cada viajero.  

🔑 **Diferenciador**: convierte campañas masivas en **experiencias personalizadas**, evitando pérdidas anuales de $250,000 y fortaleciendo la lealtad de los clientes.

---

## 📊 KPIs y Valor Generado

- **Tasa de apertura de correos**: 2% → 4%  
- **Tasa de conversión**: 1% → 1.5%  
- **Impacto esperado**:  
  - +$400,000 en ventas adicionales.  
  - Recuperación de $250,000 en pérdidas actuales.  

✅ **KPIs Clave**:  
- Incremento de tasa de conversión.  
- Aumento del ticket promedio.  
- Mejora del NPS (Net Promoter Score).  
- Crecimiento de clientes recurrentes.  
- Porcentaje de recomendaciones aceptadas/interactuadas.  

---

## ⚙️ Viabilidad Técnica

- **Estado actual**: Fase de conceptualización.  
- **Datos**: Disponibles y de calidad suficiente.  

### 🛠 Tecnologías y Hoja de Ruta
- **Exploración de Datos (EDA)** → perfiles y patrones de clientes.  
- **PoC (Proof of Concept)** → modelo base (paquete más popular). *(~1 mes)*  
- **MVP (Minimum Viable Product)** → primer motor de recomendación. *(~3 meses)*  
- **Capa de servicio (API REST con FastAPI)** → exposición de resultados.  

---

## 🗺️ Arquitectura del Sistema

```mermaid
flowchart TD
    A[Datos de Clientes y Viajes] --> B[ETL / Preprocesamiento]
    B --> C[Motor de Recomendación ML]
    C --> D[API REST con FastAPI]
    D --> E[Dashboard de Marketing]
    D --> F[Campañas de Email Personalizadas]
    F --> G[Clientes / Viajeros]
    G --> H[Interacciones y Feedback]
    H --> B
