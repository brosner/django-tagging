from tagging.managers import ModelTaggedItemManager, TagDescriptor



VERSION = (0, 4, 'pre')



class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model more than once.
    """
    pass


registry = []


def register(model, tag_descriptor_attr='tags',
             tagged_item_manager_attr='tagged'):
    """
    Sets the given model class up for working with tags.
    """

    if model in registry:
        raise AlreadyRegistered("The model '%s' has already been "
            "registered." % model._meta.object_name)
    if hasattr(model, tag_descriptor_attr):
        raise AttributeError("'%s' already has an attribute '%s'. You must "
            "provide a custom tag_descriptor_attr to register." % (
                model._meta.object_name,
                tag_descriptor_attr,
            )
        )
    if hasattr(model, tagged_item_manager_attr):
        raise AttributeError("'%s' already has an attribute '%s'. You must "
            "provide a custom tagged_item_manager_attr to register." % (
                model._meta.object_name,
                tagged_item_manager_attr,
            )
        )

    # Add tag descriptor
    setattr(model, tag_descriptor_attr, TagDescriptor())

    # Add custom manager
    ModelTaggedItemManager().contribute_to_class(model, tagged_item_manager_attr)

    # Finally register in registry
    registry.append(model)
