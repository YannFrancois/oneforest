import cv2
import numpy as np
import matplotlib.pyplot as plt

def box_to_annotation(boxes):
    """ Convert boxes as numpy array into a dictionary with all labels as Tree

    # Arguments
        box (array)    : A list of 4 elements (x1, y1, x2, y2).
    # Output
        annotations (dict) : dictionary with keys (bboxes, labels) for drawing annotations
    """
    e = np.tile("Tree", boxes.shape[0])[None].T
    annotations = {'bboxes': boxes, 'labels': e}
    return(annotations)



def draw_box(image, box, color, thickness=2):
    """ Draws a box on an image with a given color.

    # Arguments
        image     : The image to draw on.
        box       : A list of 4 elements (x1, y1, x2, y2).
        color     : The color of the box.
        thickness : The thickness of the lines to draw a box with.
    """
    b = np.array(box).astype(int)
    image = np.array(image)
    cv2.rectangle(image, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), color, thickness, cv2.LINE_AA)
    return(image)


def draw_caption(image, box, caption):
    """ Draws a caption above the box in an image.

    # Arguments
        image   : The image to draw on.
        box     : A list of 4 elements (x1, y1, x2, y2).
        caption : String containing the text to draw.
    """
    b = np.array(box).astype(int)
    cv2.putText(image, caption, (b[0], b[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
    cv2.putText(image, caption, (b[0], b[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)



def draw_boxes(image, boxes, color, thickness=2):
    """ Draws boxes on an image with a given color.

    # Arguments
        image     : The image to draw on.
        boxes     : A [N, 4] matrix (x1, y1, x2, y2).
        color     : The color of the boxes.
        thickness : The thickness of the lines to draw boxes with.
    """
    for b in boxes:
        draw_box(image, b, color, thickness=thickness)



def draw_detections(image, boxes, scores, labels, color=(255,0, 0), label_to_name=None, score_threshold=0.05):
    """ Draws detections in an image.

    # Arguments
        image           : The image to draw on.
        boxes           : A [N, 4] matrix (x1, y1, x2, y2).
        scores          : A list of N classification scores.
        labels          : A list of N labels.
        color           : The color of the boxes. By default the color from keras_retinanet.utils.colors.label_color will be used.
        label_to_name   : (optional) Functor for mapping a label to a name.
        score_threshold : Threshold used for determining what detections to draw.
    """
    selection = np.where(scores > score_threshold)[0]

    for i in selection:
        c = color if color is not None else label_color(labels[i])
        draw_box(image, boxes[i, :], color=c)


        # draw labels
        #caption = (label_to_name(labels[i]) if label_to_name else labels[i]) + ': {0:.2f}'.format(scores[i])
        #draw_caption(image, boxes[i, :], caption)


def draw_annotations(image, annotations, color=(255, 0, 0), label_to_name=None, show_caption = False):
    """ Draws annotations in an image.

    # Arguments
        image         : The image to draw on.
        annotations   : A [N, 5] matrix (x1, y1, x2, y2, label) or dictionary containing bboxes (shaped [N, 4]) and labels (shaped [N]).
        color         : The color of the boxes. By default the color from keras_retinanet.utils.colors.label_color will be used.
        label_to_name : (optional) Functor for mapping a label to a name.
    """
    if isinstance(annotations, np.ndarray):
        annotations = {'bboxes': annotations[:, :4], 'labels': annotations[:, 4]}

    assert('bboxes' in annotations)
    assert('labels' in annotations)
    assert(annotations['bboxes'].shape[0] == annotations['labels'].shape[0])

    for i in range(annotations['bboxes'].shape[0]):
        label   = annotations['labels'][i]
        c       = color if color is not None else (255,0,0)
        if show_caption:
          caption = '{}'.format(label_to_name(label) if label_to_name else label)
          draw_caption(image, annotations['bboxes'][i], caption)
        image = draw_box(image, annotations['bboxes'][i], color=c)
    plt.imshow(image)
    cv2.imshow('image',image)
    return(image)