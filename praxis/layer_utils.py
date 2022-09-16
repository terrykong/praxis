# coding=utf-8
# Copyright 2022 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provide a global list of child/children/variables created in a pax system.

To keep track of name collisions for migrating to Fiddle configuration system, a
global list of layer names etc. is being maintained.
"""

import dataclasses
import inspect

from typing import Any

pax_layer_registry = {}


@dataclasses.dataclass
class LayerInfo:
  """Layer info and conflict indication.

  Attributes:
    layer: PAX layer.
    conflict: Boolean to indicate an hparam conflict.
  """
  layer: Any
  conflict: bool = False

  def to_text(self) -> str:
    return self.layer.__class__.__name__


class LayerRegistry:
  """A dict holding information about layer creation."""

  def add_layer(self, name: str, layer: Any, conflict: bool = False) -> None:
    """Adds layer information for name to registry.

    Args:
      name: name of the layer.
      layer: the layer being created.
      conflict: the layer name has a conflict with an HParam attribute.
    """
    key = name + ' : ' + inspect.getmodule(layer).__name__
    layer_info = LayerInfo(layer=layer, conflict=conflict)
    pax_layer_registry[key] = layer_info

  def get_registry(self):
    return pax_layer_registry