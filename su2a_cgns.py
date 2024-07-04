import numpy as np
import h5py

def read_su2_mesh(file_path):
    """
    Lee un archivo de malla en formato SU2 y devuelve las coordenadas de los nodos y la conectividad de las celdas.
    """
    nodes = []
    elements = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        while lines:
            line = lines.pop(0).strip()
            if line.startswith('NDIME='):
                dim = int(line.split('=')[1])
            if line.startswith('NPOIN='):
                num_nodes = int(line.split('=')[1])
                for _ in range(num_nodes):
                    node_line = lines.pop(0).strip()
                    nodes.append(list(map(float, node_line.split()[:dim])))
            if line.startswith('NELEM='):
                num_elements = int(line.split('=')[1])
                for _ in range(num_elements):
                    elem_line = lines.pop(0).strip()
                    elements.append(list(map(int, elem_line.split()[1:])))
    return np.array(nodes), np.array(elements)

def write_cgns_mesh(file_path, nodes, elements):
    """
    Escribe los datos de la malla en un archivo en formato CGNS.
    """
    with h5py.File(file_path, 'w') as f:
        # Crear la base y la zona
        base = f.create_group('Base')
        base.attrs['CellDimension'] = 3
        base.attrs['PhysicalDimension'] = 3
        
        zone = base.create_group('Zone')
        zone.attrs['ZoneType'] = 'Unstructured'
        zone.attrs['VertexSize'] = nodes.shape[0]
        zone.attrs['CellSize'] = elements.shape[0]

        # Guardar las coordenadas de los nodos
        zone.create_dataset('GridCoordinates/CoordinateX', data=nodes[:, 0])
        zone.create_dataset('GridCoordinates/CoordinateY', data=nodes[:, 1])
        zone.create_dataset('GridCoordinates/CoordinateZ', data=nodes[:, 2])
        
        # Guardar la conectividad de los elementos
        zone.create_dataset('Elements/ElementConnectivity', data=elements)

# Leer la malla desde el archivo SU2 proporcionado
input_file = '/home/ulises/Mallas/ex1.su2'


nodes, elements = read_su2_mesh(input_file)

# Escribir la malla en un archivo CGNS
output_file = '/home/ulises/Mallas/ex2.cgns'
write_cgns_mesh(output_file, nodes, elements)

print(f'La malla se ha convertido exitosamente y guardado en {output_file}')
