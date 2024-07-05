def read_msh(filename):
    """
    Lee un archivo .msh y extrae la información de nodos y elementos.
    
    Parameters:
        filename (str): El nombre del archivo .msh.
    
    Returns:
        nodes (list): Lista de tuplas que contienen la información de los nodos (id, x, y, z).
        elements (list): Lista de tuplas que contienen la información de los elementos (id, tipo, nodos).
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    nodes = []
    elements = []
    in_nodes_section = False
    in_elements_section = False

    for line in lines:
        if line.startswith('$Nodes'):
            in_nodes_section = True
            continue
        elif line.startswith('$EndNodes'):
            in_nodes_section = False
            continue
        elif line.startswith('$Elements'):
            in_elements_section = True
            continue
        elif line.startswith('$EndElements'):
            in_elements_section = False
            continue

        if in_nodes_section:
            parts = line.split()
            if len(parts) == 4:
                # Formato del nodo: id x y z
                node_id, x, y, z = map(float, parts)
                nodes.append((node_id, x, y, z))

        if in_elements_section:
            parts = line.split()
            if len(parts) > 1:
                # Formato del elemento: id tipo nodo1 nodo2 ... nodoN
                elem_id = int(parts[0])
                elem_type = int(parts[1])
                nodes_in_element = list(map(int, parts[2:]))
                elements.append((elem_id, elem_type, nodes_in_element))

    return nodes, elements

def write_su2(filename, elements):
    """
    Escribe un archivo .su2 utilizando la información de los elementos.
    
    Parameters:
        filename (str): El nombre del archivo .su2.
        elements (list): Lista de tuplas que contienen la información de los elementos (id, tipo, nodos).
    """
    with open(filename, 'w') as f:
        # Escribir la dimensión (2D)
        f.write('NDIME= 2\n')  # Malla 2D

        # Filtrar solo los elementos 2D: Triángulos (3 nodos) y Cuadriláteros (4 nodos)
        tri_elements = [e for e in elements if e[1] == 2]  # Asumimos que el tipo 2 es un triángulo
        quad_elements = [e for e in elements if e[1] == 3]  # Asumimos que el tipo 3 es un cuadrilátero

        # Escribir el número de elementos
        f.write(f'NELEM= {len(tri_elements) + len(quad_elements)}\n')
        
        # Escribir los elementos triangulares
        for elem in tri_elements:
            elem_id, elem_type, nodes_in_elem = elem
            node_indices = ' '.join(str(n-1) for n in nodes_in_elem)  # Indices en SU2 son basados en cero
            f.write(f'{elem_id-1} TRIANGLE {node_indices} 0\n')  # Asumimos marcador 0, ajustar según sea necesario

        # Escribir los elementos cuadriláteros
        for elem in quad_elements:
            elem_id, elem_type, nodes_in_elem = elem
            node_indices = ' '.join(str(n-1) for n in nodes_in_elem)  # Indices en SU2 son basados en cero
            f.write(f'{elem_id-1} QUADRILATERAL {node_indices} 0\n')  # Asumimos marcador 0, ajustar según sea necesario

def convert_msh_to_su2(msh_filename, su2_filename):
    """
    Convierte un archivo .msh a un archivo .su2.
    
    Parameters:
        msh_filename (str): El nombre del archivo .msh.
        su2_filename (str): El nombre del archivo .su2.
    """
    # Leer el archivo .msh para obtener nodos y elementos
    nodes, elements = read_msh(msh_filename)
    # Escribir los datos en un archivo .su2
    write_su2(su2_filename, elements)

# Convertir el archivo input.msh a suj.su2
convert_msh_to_su2('input.msh', 'suj.su2')

