import gmsh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import webbrowser

def read_msh(filename):
    """Lee el archivo .msh utilizando gmsh"""
    gmsh.initialize()
    gmsh.open(filename)
    nodes = gmsh.model.mesh.getNodes()
    elements = gmsh.model.mesh.getElements()
    gmsh.finalize()

    node_coords = nodes[1].reshape(-1, 3)
    element_types = elements[0]
    element_tags = elements[1]
    element_nodes = [elements[2][i].reshape(-1, 3) for i in range(len(element_types)) if element_types[i] == 2]

    return node_coords, element_nodes[0] if element_nodes else []

def write_unv_using_gmsh(input_filename, output_filename):
    """Escribe el archivo .unv utilizando la API de gmsh"""
    gmsh.initialize()
    gmsh.open(input_filename)
    gmsh.write(output_filename)
    gmsh.finalize()

def explain_mesh(node_coords, elements):
    """Explica los nodos y elementos de la malla"""
    print(f"Número de nodos: {len(node_coords)}")
    print("Nodos (primeros 5 nodos):")
    for i, node in enumerate(node_coords[:5]):
        print(f" Nodo {i+1}: ID={i+1}, Coordenadas=({node[0]}, {node[1]}, {node[2]})")

    print(f"\nNúmero de elementos: {len(elements)}")
    print("Elementos (primeros 5 elementos):")
    for i, element in enumerate(elements[:5]):
        print(f" Elemento {i+1}: ID={i+1}, Nodos={element}")

def visualize_mesh(node_coords, elements):
    """Visualiza la malla utilizando matplotlib"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(node_coords[:, 0], node_coords[:, 1], node_coords[:, 2], marker='o')

    for element in elements:
        tri = node_coords[element - 1]  # Ajustar índices a base 0
        tri = np.vstack((tri, tri[0]))  # cerrar el triángulo
        ax.plot(tri[:, 0], tri[:, 1], tri[:, 2], 'r-')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


def interactive_menu():
    """Muestra un menú interactivo para el usuario"""
    while True:
        print("\nOpciones:")
        print("1. Explicar malla")
        print("2. Visualizar malla")
        print("3. Convertir archivo .msh a .unv")
   
        print("6. Salir")
        
        choice = input("Selecciona una opción: ")
        
        if choice == '1':
            explain_mesh(node_coords, elements)
        elif choice == '2':
            visualize_mesh(node_coords, elements)
       
        elif choice == '3':
            unv_filename = input("Introduce el nombre del archivo de salida (.unv): ")
            write_unv_using_gmsh(msh_filename, unv_filename)

        elif choice == '6':
            break
        else:
            print("Opción no válida, intenta de nuevo.")

def main():
    global node_coords, elements, msh_filename


    msh_filename =input("ingrese el nombre del archivo.msh: ")
    node_coords, elements = read_msh(msh_filename)

    interactive_menu()

if __name__ == "__main__":
    main()

