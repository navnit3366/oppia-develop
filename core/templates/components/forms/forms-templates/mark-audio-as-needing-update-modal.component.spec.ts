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
 * @fileoverview Unit Test for Mark Audio As Needing Update Modal Component.
 */

import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, waitForAsync, TestBed } from '@angular/core/testing';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { MarkAudioAsNeedingUpdateModalComponent } from './mark-audio-as-needing-update-modal.component';

class MockActiveModal {
  close(): void {
    return;
  }

  dismiss(): void {
    return;
  }
}

describe('Delete Exploration Modal Component', () => {
  let component: MarkAudioAsNeedingUpdateModalComponent;
  let fixture: ComponentFixture<MarkAudioAsNeedingUpdateModalComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [
        MarkAudioAsNeedingUpdateModalComponent
      ],
      providers: [{
        provide: NgbActiveModal,
        useClass: MockActiveModal
      }],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents();

    fixture = TestBed.createComponent(MarkAudioAsNeedingUpdateModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should check whether component is initialized', () => {
    expect(component).toBeDefined();
  });
});
