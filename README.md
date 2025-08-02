## Cubo ladilloso en openGL (el cubo me odia mas de lo que yo lo odio a el)

pss nose la verdad es la primera vez que hago algo con openGL asi que si alguien consigue este repositorio
lo que vera ahi es un cochinero, pero bueno nada lo hice mientras tenia flojera y me distraje chorrocientas veces

### Requisitos
- Python3
- Estudiar una materia de un profesor que pide cosas ladillas
- nose

### Inicializar

- Cuando clones el proyecto metete en la carpeta y crea un venv

```
 python -m venv myenv
```
Y lo ejecutas:
  
  Si estas en Windows:
  ```
  .\myenv\Scripts\activate
  ```
  Si estas en un Unix Like:
  ```
  source myenv/bin/activate
  ```

### Dependencias del Proyecto
- Pygame
- PyOpenGL

Ejecuta dentro del venv:
```
pip install pygame PyopenGL
```

## Instrucciones de uso

Hay 6 imagenes en dentro de la carpeta [Cara1...6.png] y cada una corresponde a una cara del cubo (dah)
enfin, reemplazalas con cualquier imagen pero tienen que llamarse igual "cara{numero que corresponde a la cara del cubo}.png"

- Las imagenes tienen que ser de 1024 x 1024
- Te recomiendo que pongas en "cara5.png" la que es tu cara6 y en "cara6.png" coloques a cara5 porque deje el orden de las transiciones choreto
  y te lleva primero a la cara 6 y por ultimo a la 5, tipo orden(1, 2, 3, 4, 6, 5)
  podria haberlo reparado pero me dio flojera, asi que ten eso en cuenta o si eres bien proactivo puedes reparar eso lmao

  y creo q ya(?

