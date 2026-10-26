# Aventura Eléctrica — guía interactiva de 4.º

Sitio educativo estático en español sobre artefactos y circuitos básicos. Incluye simulador 3D, laboratorio 2D, retos, recursos docentes y diez modelos GLB originales de bajo poligonaje.

## Ejecutar en tu computador

El visor GLB necesita que los archivos se sirvan por HTTP; abrir `index.html` directamente como `file://` puede bloquear la carga de modelos en algunos navegadores.

1. Descomprime el ZIP.
2. Entra a la carpeta `guia-interactiva-grado4`.
3. Ejecuta `python -m http.server 8000`.
4. Abre `http://localhost:8000` en el navegador.

También puedes subir el contenido de esta carpeta a la raíz de un repositorio y habilitar GitHub Pages desde la rama principal. Los modelos usan rutas relativas y quedarán dentro de `assets/models/`.

## Dependencias en el navegador

La página carga Tailwind CSS, Three.js, Chart.js, `<model-viewer>` y las fuentes desde CDNs. Se requiere conexión a internet para esas bibliotecas. Los diez archivos `.glb` sí están incluidos localmente en el repositorio.

## Modelos 3D

El selector permite ver y rotar: pila AA, interruptor, bombillo incandescente, LED, cable de cobre, aluminio, mina de grafito, regla de plástico, borrador de nata y palito de madera. Son mallas educativas ilustrativas de bajo poligonaje; no son CAD, no tienen escala de fabricación y no deben usarse como planos de componentes reales.

Puedes recrearlos con Python estándar:

```bash
python scripts/generate_models.py
python scripts/validate_models.py
```

## Alcance educativo y seguridad

Las animaciones de corriente, voltaje, conductividad y eficiencia son comparaciones cualitativas; no son mediciones de laboratorio. El circuito LED no simula polaridad ni resistencia limitadora. Trabaja solo con pilas de baja tensión y con acompañamiento adulto; nunca conectes el experimento a un tomacorriente. El contenido curricular es una propuesta para revisar frente a las fuentes oficiales vigentes del MEN y el PEI institucional.

El botón de cámara solo usa el video como fondo detrás del circuito. No implementa WebXR, seguimiento espacial ni anclaje de objetos.
