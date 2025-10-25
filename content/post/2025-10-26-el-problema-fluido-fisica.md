---
title: El problema de la mecánica de fluído en física
subtitle: Simplifcaciones que son inexistentes
date: 2025-10-26T00:00:00-04:00
draft: true
image: img/2025-06-30-memorizacion.jpg
tags:
  [
    "Fluído Incompresible",
    "Fluído Ideal",
    "Preconcepciones",
    "Calidad Educativa",
  ]
---

La mecánica de fluidos es una de esas áreas de la física descuidada por los físicos. En muchos programas de grado de física esta disciplina ni siquiera se ofrece como optativa. En este artículo vamos a resaltar una graves deficiencias en cómo se trata la mecánica de fluídos a nivel de física general, en donde los libros introducen errores conceptuales a jóvenes físicos e ingenieros.

## El problema del concepto de fluído ideal

El problema central de la dinámica de fluído en como se trata en los libros de textos de física general y en textos más elementales, es en el conepto de fluído ideal, que es aquel que tiene las siguientes propiedades:

1. Es incompresible
2. Carece de viscosidad

Resulta ser que estas dos propiedades son, en la práctica, completamente incompatible, así que es imposible encontrar un fluído en la naturaleza que se aproxime razonablemente a estas dos propiedades para que se pueda considerar ideal.

Si un fluído es incompresible, es definitivamente un líquido, lo que implica que su viscosidad no puede ser despreciable. Así que no existen ejemplos de sustancias reales que cumplan estas dos propiedades.

Si el fluído no es viscoso, entonces definitivamente tiene que estar en estado gaseoso, lo cual lo hace suceptible a ser comprimido.

Así que tenemos libros llenos de ejercicios de estos fluídos que son inexistentes, y «aprendiendo» cosas que no son reales ni existen.

La ecuación que explica el movimiento de un fluído incompresible y sin viscosidad es:
$$P + \rho g y + \dfrac{1}{2}\rho v^2 = \text{constante} $$

aquí tanto la presión, la altura y la densidad de energía cinética se miden en un mismo punto. La cantidad aquí interesante es la velocidad, la cual se considera que es fija, pero como veremos más adelante, esta rapidez tiende a ser mayor mientras más lejos del contenedor está el punto en donde se mide.

## La viscosidad es importante

Resulta ser que para comprender muchas propiedades de los fluídos, tanto en reposo como en movimiento, es necesario tener un entendimiento al menos rudimentario de la viscosidad.

Uno de los hechos más importante de la viscosidad es que la primera capa de un fluído en contato con una superficie en reposo _no se mueve_, creando así una de las condiciones de fronteras más importante que debe comprender un físico sobre los fluídos. Pero si un fluido no es viscoso, entonces esta primera capa podría moverse, permitiendo una distribución de velocidad uniforme a través de todo el tubo de flujo.

Así que la cantidad $v$ que aparece en la ecuación de Bernouilli es fija, por lo que es una rapidez «eficaz», para lo cual también aplica un área de sección transversal efectiva, la cual debe ser definida para que pueda ser medido.

Así que seguramente muchos físicos creen que la velocidad de la superficie de un río es la misma que en el fondo del río, cuando se sabe que, generalmente, no es así. Al acercarte el fondo del río, mejor es la velocidad del agua, porque el agua en contacto con el agua debe estar en reposo.

## La variación de la densidad de los gases es importante

Ahora consideremos el movimiento de un gas, en donde la viscosidad si se puede argumentar que es pequeña y se puede despreciar para fines prácticos. Pero ahora el gas debe ser _compresible_ lo que implica que un aumento en la presión implica un amento en la densidad del gas. Este comportamiento es importante, porque sabemos que la temperatura, la presión y la densidad de un gas es bastante conocido (aunque es para cuando el gas está en equilibrio... pero no nos distraigamos, porque este es otra caja de pandora)

Un aspecto interesnte de los gases es que sus propiedades, incluyendo la viscosidad, varía bastante con el cambio de temperatura, la cual también varía con el cambio de densidad, ya que estos aumentos en lo que puede resultar muy fácil salirse de los parámetros de viscosidad baja.

## ¿Por qué se hace esta simplificación?

Aquí creo que voy a especular un poco. Creo que estos conceptos errados se han introducido para tratar de hacer la el tema más simple, ya que la ecuación de Bernoulli se vuelve intractable para fluídos reales. Aunque entiendo la disjuntiva, creo que los efectos negativos en la comprensión de los fluidos en los estudiantes de física y de ingenier
