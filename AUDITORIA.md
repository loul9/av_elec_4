# Auditoría técnica y correcciones

## Hallazgos corregidos

- La interfaz prometía zoom en el visor de Three.js, pero no había control de zoom. Ahora la rueda permite acercar/alejar; el visor individual `<model-viewer>` también permite rotar y hacer zoom táctil.
- El botón llamado “Realidad Aumentada” solo pedía permiso de cámara y ponía el video detrás de un modelo fijo. Se renombró y se aclaró que es un fondo de cámara, no WebXR ni RA espacial. Se cubren permisos denegados, navegador sin cámara, contexto inseguro y cancelación de una solicitud pendiente; al apagar, se detienen las pistas de video.
- Seleccionar LED cambiaba el texto y el color de una esfera de bombillo: no existía un modelo LED visible. El circuito ahora alterna entre bombillo y un LED con lente y terminales separados.
- El grafito se trataba igual que el cobre y el aluminio. Se representa ahora como conductor de menor intensidad y la explicación señala que es una comparación cualitativa.
- El diagnóstico del laboratorio 2D nunca cambiaba y las partículas solo recorrían el tramo superior. El diagnóstico responde al interruptor/material; los puntos recorren el contorno completo, con espacio para la pila, y su velocidad varía cualitativamente.
- El voltaje podía mostrar varias pilas mientras el dibujo parecía una sola. La etiqueta de la fuente ahora muestra la cantidad simulada de pilas AA y su voltaje.
- La barra de navegación no indicaba qué sección estaba activa. Se sincronizaron las pestañas de escritorio y móvil, y se permite búsqueda de la matriz sin distinguir tildes.
- La vista móvil bloqueaba el zoom del navegador. Se quitó la restricción `user-scalable=no`.
- Las respuestas del cuestionario se expresaban de forma demasiado concluyente. La pregunta de la linterna ahora pregunta por una posible causa; la comparación de LED evita afirmar que siempre son más eficientes en todos los usos.
- La gráfica comparaba un zumbador con bombillos usando porcentajes sin fuente. Se retiró el zumbador de esa comparación y se etiqueta el ejemplo como ilustrativo, no como medición.
- Se corrigieron errores de escritura, se añadió un mensaje de seguridad para pilas de baja tensión y se rebajó la afirmación de que la matriz es una orientación oficial verificada: el contenido debe contrastarse con la fuente MEN vigente y el PEI.

## Límites que permanecen

- La cámara no hace seguimiento ni coloca el circuito en una superficie real; una experiencia WebXR completa sería otro desarrollo.
- La física del circuito es conceptual. No simula resistencia cuantitativa, polaridad del LED, resistencias limitadoras, pérdidas medidas ni condiciones reales de humedad/material.
- Los porcentajes de energía útil/calor son ejemplos orientativos y dependen del dispositivo. Deben sustituirse por mediciones y fuentes si se usan como datos científicos.
- La página carga Tailwind, Three.js, Chart.js, model-viewer y fuentes mediante CDNs; requiere conexión para estas bibliotecas. Los modelos GLB están incluidos localmente.
- Se probó en Chromium headless sobre servidor local: carga de los diez GLB, alternancia del LED, apertura/cierre del circuito, búsqueda de la matriz sin tildes, navegación y respuestas del cuestionario; no se observaron excepciones JavaScript. También se verificó la disposición móvil a 390 px sin desbordamiento horizontal.
- No se probó el permiso real de cámara en un dispositivo físico ni compatibilidad con Safari móvil. Antes de publicar, revisa esos casos en el hardware objetivo.

## Pruebas incluidas

`python scripts/validate_models.py` valida la cabecera y la estructura GLB 2.0 de los diez modelos incluidos. `node --check` sobre el JavaScript extraído de `index.html` comprueba sintaxis; la prueba Chromium anterior cubre las interacciones principales, pero no reemplaza una comprobación en un teléfono real.
