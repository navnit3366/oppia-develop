// Copyright 2021 The Oppia Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Component for the filtering choices.
 */

import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'oppia-filtered-choices-field',
  templateUrl: './filtered-choices-field.component.html'
})
export class FilteredChoicesFieldComponent {
  // These properties are initialized using Angular lifecycle hooks
  // and we need to do non-null assertion. For more information, see
  // https://github.com/oppia/oppia/wiki/Guide-on-defining-types#ts-7-1
  @Input() choices!: string[];
  @Input() selection!: string;
  @Input() placeholder!: string;
  @Input() searchLabel: string = 'search';
  @Input() isSearchable?: boolean = true;
  @Input() noEntriesFoundLabel: string = 'No matches found';
  @Output() selectionChange: EventEmitter<string> = (
    new EventEmitter());

  filteredChoices!: string[];

  ngOnInit(): void {
    this.filteredChoices = this.choices;
  }

  filterChoices(searchTerm: string): void {
    this.filteredChoices = this.choices.filter(
      choice => choice.toLowerCase().indexOf(searchTerm.toLowerCase()) > -1);
  }

  updateSelection(selection: string): void {
    this.selection = selection;
    this.selectionChange.emit(selection);
  }
}