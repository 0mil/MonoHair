import struct
import bpy

def load_strand(file):
    print("Opening file...")
    with open(file, mode='rb') as f:
        print("Reading number of strands...")
        num_strand = f.read(4)
        (num_strand,) = struct.unpack('I', num_strand)
        print(f"Number of strands: {num_strand}")
        
        print("Reading point count...")
        point_count = f.read(4)
        (point_count,) = struct.unpack('I', point_count)
        print(f"Point count: {point_count}")
        
        print("Reading segments...")
        segments = f.read(2 * num_strand)
        segments = struct.unpack('H' * num_strand, segments)
        segments = list(segments)
        print(f"Segments read: {len(segments)} segments")
        
        print("Reading points...")
        num_points = sum(segments)
        points = f.read(4 * num_points * 3)
        points = struct.unpack('f' * num_points * 3, points)
        print(f"Number of points read: {num_points}")
    
    print("Processing points...")
    points = list(points)
    points = [points[i:i+3] for i in range(0, len(points), 3)]
    print("Points processing completed.")
    
    data = {
        "num_strand": num_strand,
        "segments": segments,
        "points": points
    }
    
    return data

def create_single_curve_from_data(data):
    print("Starting to create curve from data...")
    segments = data['segments']
    points = data['points']
    
    curve_data = bpy.data.curves.new(name='HairCurve', type='CURVE')
    curve_data.dimensions = '3D'
    curve_obj = bpy.data.objects.new('HairObject', curve_data)
    bpy.context.collection.objects.link(curve_obj)
    
    point_index = 0
    total_segments = len(segments)
    print(f"Total segments to process: {total_segments}")
    
    for seg_idx, seg in enumerate(segments):
        polyline = curve_data.splines.new('POLY')
        polyline.points.add(seg - 1)
        
        for i in range(seg):
            x, y, z = points[point_index]
            polyline.points[i].co = (x, y, z, 1)
            point_index += 1
        
        if (seg_idx + 1) % 10 == 0 or (seg_idx + 1) == total_segments:
            print(f"Processed {seg_idx + 1}/{total_segments} segments")
    
    print("Curve creation completed.")

# Set file path (Update this path according to your system)
file_path = r'path_to_your_hair_file/connected_strands.hair'

# load data from binary .hair file
print("Starting the process...")
data = load_strand(file_path)

# generate curve object
create_single_curve_from_data(data)
print("Process completed.")
