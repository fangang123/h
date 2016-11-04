'use strict';

var ConfirmSubmitController = require('../../controllers/confirm-submit-controller');
var util = require('./util');

describe('ConfirmSubmitController', function () {

  var ctrl;

  afterEach(function () {
    if (ctrl) {
      ctrl.element.remove();
      ctrl = null;
    }
  });

  /**
   * Make a <button type="submit"> with the confirm submit controller
   * enhancement applied and return the various parts of the component.
   *
   */
  function component(windowConfirmReturnValue) {
    var confirmMessage = "Are you sure you want to leave the group 'Test Group'?";
    var template = [
      '<button type="submit"',
      '        class="js-confirm-submit"',
      '        data-confirm-message="' + confirmMessage + '">',
    ].join('\n');

    var fakeWindow = {
      confirm: sinon.stub().returns(windowConfirmReturnValue),
    };

    ctrl = util.setupComponent(document,
                               template,
                               ConfirmSubmitController,
                               {window: fakeWindow});

    return {
      ctrl: ctrl,
      fakeWindow: fakeWindow,
      confirmMessage: confirmMessage,
    };
  }

  function fakeEvent() {
    var event = new Event('click');
    event.preventDefault = sinon.stub();
    event.stopPropagation = sinon.stub();
    event.stopImmediatePropagation = sinon.stub();
    return event;
  }

  it('shows a confirm dialog using the text from the data-confirm-message attribute', function () {
    var {ctrl, fakeWindow, confirmMessage} = component(true);

    ctrl.element.dispatchEvent(new Event('click'));

    assert.isTrue(fakeWindow.confirm.calledOnce);
    assert.calledWithExactly(fakeWindow.confirm, confirmMessage);
  });

  it('prevents form submission if the user refuses the confirm dialog', function () {
    var ctrl = component(false).ctrl;
    var event = fakeEvent();

    ctrl.element.dispatchEvent(event);

    assert.isTrue(event.preventDefault.called);
    assert.isTrue(event.stopPropagation.called);
    assert.isTrue(event.stopImmediatePropagation.called);
  });

  it('allows form submission if the user confirms the confirm dialog', function () {
    var ctrl = component(true).ctrl;
    var event = fakeEvent();

    ctrl.element.dispatchEvent(event);

    assert.isFalse(event.preventDefault.called);
    assert.isFalse(event.stopPropagation.called);
    assert.isFalse(event.stopImmediatePropagation.called);
  });
});
