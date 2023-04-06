def image_checker(image_name):
    import cv2
    import argparse
    import numpy as np
    # handle command line arguments
    ap = argparse.ArgumentParser()
    image="graphs/"+image_name
    cfg="dots.cfg"
    weights="dots_last.weights"
    classesfile="dots.names"
    # read input image
    image = cv2.imread(image,cv2.IMREAD_UNCHANGED)

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    classes = None
    with open(classesfile, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNet(weights, cfg)


    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)


    net.setInput(blob)



    def get_output_layers(net):
        layer_names = net.getLayerNames()

        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

        return output_layers



    def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
        label = str(classes[class_id])

        color = COLORS[class_id]

        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.putText(img, str(confidence)[:3], (x +50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


    outs = net.forward(get_output_layers(net))
    # initialization
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.1
    nms_threshold = 0.4


    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        i = i
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        draw_bounding_box(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
    # image=cv2.resize(image,(1500,1000))
    # display output image
    if 0 in class_ids and 1 in class_ids and 2 in class_ids:
        cv2.imwrite("good_graphs/"+image_name,image)
    else:
        print("not enough markers")

